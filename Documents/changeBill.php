<head>
<script src="js/jquery-1.9.1.js"></script>
<script src="js/jquery-ui.js"></script>
<script src="js/changeBill.js"></script>
</head>
<body>
<input type='hidden' id="billName" value='<?php echo $_GET['bill']; ?>'>
<input type='hidden' id="billDate" value='<?php echo $_GET['date']; ?>'>
	<form id='editBill'>
		<label for='bill'>Bill:</label><input type='text' name='bill' id='bill'><br />
		<label for='amount'>Amount:</label><input type='text' name='amount' id='amount'><br />
		<input type="radio" value='Paid' name="billStatus" id="r_Paid">Paid
		<input type="radio" value='Due' name="billStatus" id="r_Due">Due
		<input type="radio" value='Skip' name="billStatus" id="r_Skip">Skip<br />
		<input type="radio" value='Automatic' name="status" id="r_Auto">Automatic
		<input type="radio" value='Manual' name="status" id="r_Manual">Manual<br>
		<select id='pay_method'></select><br />
		<button id="button">Change Bill</button>
	</form>
</body>
