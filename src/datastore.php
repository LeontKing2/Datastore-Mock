<?php
#Signed By ARD at 19:17 IST.
if ($_GET["scope"] && $_GET["name"]) {
    $scope = $_GET["scope"];
    $name = $_GET["name"];
    $filename = "datastore/" . $scope . "/" . $name . ".json";
    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        $data = json_decode(file_get_contents('php://input'), true);
        if ($data) {
            if (!file_exists(dirname($filename))) {
                mkdir(dirname($filename), 0777, true);
            }
            file_put_contents($filename, json_encode($data));
            http_response_code(204);
        } else {
            http_response_code(400);
        }
    } else {
        if (file_exists($filename)) {
            $data = json_decode(file_get_contents($filename), true);
            echo json_encode($data);
        } else {
            http_response_code(404);
        }
    }
} else {
    http_response_code(400);
}
?>
