<?php
    $servername = 'localhost';
    $username = 'root';
    $password = '';
    $db = 'todaysStocks';
    
    $full_db = new mysqli($servername, $username, $password, $db);
    $full_db->set_charset('utf8');
    
    $stocks = [];
    $query = 'SELECT rank, title, volume, price, cng, perc_cng FROM `2017-04-19`';
    
    if ($stmt = $full_db->prepare($query)) {
		$stmt->execute();
		$result = $stmt->get_result();
		$stmt->free_result();
		$stmt->close();
		while ($row = $result->fetch_array(MYSQLI_ASSOC)) {
			$stockDetails[] = [
				"rank"      => $row['rank'],
				"title"     => $row['title'],
				"volume"    => $row['volume'],
				"price"     => $row['price'],
				"cng"      => $row['cng'],
				"perc_cng" => $row['perc_cng']
			];
		}
	}

?>

<html>
    <head>
        <meta charset='UTF-8'>
        <title>STOCKS</title>
        <style>
            th { text-align: left }
            th,td { min-width: 100px; padding-left: 20px }
            th:first-child, td:first-child { padding-left: 0; text-align: center }
        </style>
    <head>
    
    <body>
        <table>
        <thead>
            <tr>
                <th>RANK</th>
                <th>TITLE</th>
                <th>VOLUME</th>
                <th>PRICE</th>
                <th>CHANGE</th>
                <th>% CHANGE</th>
            </tr>
        </thead>
        <?php
            foreach ($stockDetails as $details) {
                echo "<tr>" .
                        "<td>" . $details['rank'] . "</td>" .
                        "<td>" . $details['title'] . "</td>" .
                        "<td>" . $details['volume'] . "</td>" .
                        "<td>" . $details['price'] . "</td>" .
                        "<td>" . $details['cng'] . "</td>" .
                        "<td>" . $details['perc_cng'] . "</td>" .
                     "</tr>";
            }
        ?>
        </table>
    </body>
</html>
