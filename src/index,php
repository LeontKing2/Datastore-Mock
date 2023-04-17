<?php
$method = $_SERVER['REQUEST_METHOD'];
$request = explode('/', trim($_SERVER['PATH_INFO'],'/'));
$datastore_scope = array_shift($request);
$datastore_name = array_shift($request);

if ($method == 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);
    if (!is_array($data)) {
        http_response_code(400);
        echo json_encode(array('error' => 'Invalid JSON data'));
        exit;
    }
    $filename = $datastore_scope . '_' . $datastore_name . '_' . $request[0] . '.json';
    if (!file_exists($filename)) {
        file_put_contents($filename, '{}');
    }
    $json = json_decode(file_get_contents($filename), true);
    $json[$request[0]] = $data;
    file_put_contents($filename, json_encode($json));
    echo json_encode(array('success' => true));
} elseif ($method == 'GET') {
    $filename = $datastore_scope . '_' . $datastore_name . '_' . $request[0] . '.json';
    if (!file_exists($filename)) {
        echo json_encode(array('error' => 'DataStore not found'));
        exit;
    }
    $json = json_decode(file_get_contents($filename), true);
    if (isset($request[1])) {
        echo json_encode($json[$request[1]]);
    } else {
        echo json_encode($json);
    }
} else {
    http_response_code(405);
    header('Allow: GET, POST');
    echo json_encode(array('error' => 'Method not allowed'));
}
?>
