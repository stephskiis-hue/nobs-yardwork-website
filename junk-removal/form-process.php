<?php
/**
 * form-process.php — handles the quote form on quote.html.
 *
 * Adapted from the handler on no-bs-yardwork.com. Differences:
 *   - fields match the junk removal quote form
 *   - redirects to thanks.html instead of echoing a string, so the form works
 *     with a plain POST and needs no JavaScript
 *   - honeypot field silently drops obvious bots
 *   - header injection guard on the values that reach the mail headers
 *
 * The host runs ea-php70, so this stays deliberately plain.
 *
 * DELIVERABILITY: PHP mail() on shared hosting often lands in spam. Send
 * yourself a test the day this goes live, and check the junk folder. If it is
 * unreliable, swap the form on quote.html for the JotForm embed — the README
 * has the snippet.
 */

$to      = 'nobsyardwork@gmail.com';
$subject = 'Junk Removal Quote Request';

// Bots fill in every field they find; humans never see this one.
if (!empty($_POST['website'])) {
    header('Location: thanks.html');
    exit;
}

function field($key) {
    return isset($_POST[$key]) ? trim($_POST[$key]) : '';
}

$name      = field('name');
$phone     = field('phone');
$email     = field('email');
$postal    = field('postal');
$preferred = field('preferred');
$jobtype   = field('jobtype');
$details   = field('details');

$errors = array();
if ($name === '')    { $errors[] = 'name'; }
if ($phone === '')   { $errors[] = 'phone'; }
if ($details === '') { $errors[] = 'details'; }
if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) { $errors[] = 'email'; }

if (!empty($errors)) {
    header('Location: quote.html?error=1#quote-form');
    exit;
}

// Never let a submitted value break out into the mail headers.
$safe_email = preg_replace('/[\r\n]+/', ' ', $email);
$safe_name  = preg_replace('/[\r\n]+/', ' ', $name);

$body  = "New junk removal quote request\n\n";
$body .= "Name:           " . $name . "\n";
$body .= "Phone:          " . $phone . "\n";
$body .= "Email:          " . $email . "\n";
$body .= "Postal code:    " . ($postal !== '' ? $postal : '-') . "\n";
$body .= "Preferred date: " . ($preferred !== '' ? $preferred : '-') . "\n";
$body .= "Job type:       " . ($jobtype !== '' ? $jobtype : '-') . "\n\n";
$body .= "What they're getting rid of:\n" . $details . "\n\n";
$body .= "-- \nSent from no-bs-junkremoval.com\n";

$headers  = "From: No BS Junk Removal <" . $to . ">\r\n";
$headers .= "Reply-To: " . $safe_name . " <" . $safe_email . ">\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

@mail($to, $subject, $body, $headers);

// Redirect either way — a mail() failure is ours to chase in the logs, not
// something to show a customer who has already given us their number.
header('Location: thanks.html');
exit;
