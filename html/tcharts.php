<!DOCTYPE html>
<html lang="es">
<head>
	<script src="https://code.highcharts.com/highcharts.js"></script>
	<script src="https://code.highcharts.com/modules/exporting.js"></script>
	<script src="https://code.highcharts.com/modules/export-data.js"></script>

</head>
<body>


<?php
$dbconn = pg_connect("host=localhost dbname=monitoreo user=root password=hola123") or die('No se ha podido conectar: ' . pg_last_error());
?>

<div id="graph" style="width:600px;height:250px;"></div>

<script>
Highcharts.chart('graph', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Distribucion de Gestores de contenido'
    },
    xAxis: {
    	type: 'category'

    },
    credits: {
        enabled: false
    },
    series: [{
        name: 'CMS',
<?php echo "data: [";
$query = "SELECT count(*),cms FROM servicio s,domser ds, dominio d where d.iddominio = ds.iddominio and s.idservicio = ds.idservicio group by cms";
$cmss = pg_query($query) or die('La consulta fallo: ' . pg_last_error()); 
$arr = pg_fetch_row($cmss);
do{
	echo "['$arr[1]',$arr[0]],";
} while($arr = pg_fetch_row($cmss));

echo "]" ;?>
    }]
});
</script>



<div id="top5" style="width:600px;height:250px;"></div>

<script>
Highcharts.chart('top5', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Top 5 CMS\'s mas usados'
    },
    xAxis: {
    	type: 'category'

    },
    credits: {
        enabled: false
    },
    series: [{
        name: 'CMS',
<?php echo "data: [";
$query = "SELECT count(*),cms FROM servicio s,domser ds, dominio d where d.iddominio = ds.iddominio and s.idservicio = ds.idservicio group by cms limit 5";
$cmss = pg_query($query) or die('La consulta fallo: ' . pg_last_error()); 
$arr = pg_fetch_row($cmss);
do{
	echo "['$arr[1]',$arr[0]],";
} while($arr = pg_fetch_row($cmss));

echo "]" ;?>
    }]
});
</script>
<div id="Cont" style="width:600px;height:250px;"></div>

<script>
Highcharts.chart('Cont', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Tipos de contenidos'
    },
    xAxis: {
    	type: 'category'

    },
    credits: {
        enabled: false
    },
    series: [{
        name: 'CMS',
<?php echo "data: [";
$query = "SELECT count(*),s.nombre FROM servicio s,domser ds, dominio d where d.iddominio = ds.iddominio and s.idservicio = ds.idservicio group by s.nombre";
$cmss = pg_query($query) or die('La consulta fallo: ' . pg_last_error()); 
$arr = pg_fetch_row($cmss);
do{
	echo "['$arr[1]',$arr[0]],";
} while($arr = pg_fetch_row($cmss));

echo "]" ;?>
    }]
});
</script>



<?php pg_close($dbconn) ?>



</body>
