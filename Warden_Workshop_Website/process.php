<?php
// Check if the form was actually submitted via POST
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    // 1. Sanitize and gather the form data
    $name    = strip_tags(trim($_POST["name"]));
    $email   = filter_var(trim($_POST["email"]), FILTER_SANITIZE_EMAIL);
    $phone   = strip_tags(trim($_POST["phone"]));
    $service = strip_tags(trim($_POST["service"]));
    $message = trim($_POST["message"]);

    // 2. Validate the data (ensure nothing empty slipped through)
    if (empty($name) || empty($message) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        // If data is missing or email is invalid, send them back
        header("Location: contact.html?status=error");
        exit;
    }

    // 3. Set up the email recipient and subject
    $recipient = "apwarden1@gmail.com";
    $subject   = "New Project Inquiry from $name - Warden's Workshop";

    // 4. Build the email body
    $email_content  = "You have received a new project inquiry from the Warden's Workshop website.\n\n";
    $email_content .= "Client Details:\n";
    $email_content .= "------------------------\n";
    $email_content .= "Name: $name\n";
    $email_content .= "Email: $email\n";
    $email_content .= "Phone: $phone\n\n";
    $email_content .= "Project Category: $service\n\n";
    $email_content .= "Project Details:\n";
    $email_content .= "------------------------\n";
    $email_content .= "$message\n";

    // 5. Build the email headers
    $email_headers = "From: $name <$email>";

    // 6. Send the email using PHP mail()
    if (mail($recipient, $subject, $email_content, $email_headers)) {
        // Success! Redirect to the Thank You page
        header("Location: thank-you.html");
        exit;
    } else {
        // Server failed to send email
        header("Location: contact.html?status=server_error");
        exit;
    }

} else {
    // If someone tries to visit process.php directly, redirect them to the home page
    header("Location: index.html");
    exit;
}
?>