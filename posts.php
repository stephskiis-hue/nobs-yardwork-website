<?php
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: public, max-age=300');
header('Access-Control-Allow-Origin: *');
$file = __DIR__ . '/posts.json';
echo file_exists($file) ? file_get_contents($file) : '[]';
