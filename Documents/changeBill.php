<head>
	<script src="js/jquery-1.9.1.js"></script>
	<script src="js/jquery-ui.js"></script>
	<script src="js/changeBill.js"></script>
<style>
	fieldset {
  		padding: 1em;
	  	margin-bottom: 10px;
	}
</style>
</head>
<body>
<input type='hidden' id="billName" value='<?php echo $_GET['bill']; ?>'>
<input type='hidden' id="billDate" value='<?php echo $_GET['date']; ?>'>
	<form id='editBill'>
		<div style='margin-bottom: 10px;'>
			<label for='bill' style="float: left; margin-left: 40%;">Bill:</label><input type='text' name='bill' id='bill' disabled='disabled'><br />
		</div>
		<fieldset>
			<label for='amount' style="float: left; margin-left: 37%;">Amount:</label><input type='text' name='amount' id='amount'><br />
		</fieldset>
		<fieldset>
		   <div style="float: left; margin-left: 37%">
			<input type="radio" value='Paid' name="billStatus" id="r_Paid">Paid
			<input type="radio" value='Due' name="billStatus" id="r_Due">Due
			<input type="radio" value='Skip' name="billStatus" id="r_Skip">Skip<br />
		   </div>
		</fieldset>
		<fieldset>
		   <div style='float: left; margin-left: 31%'>
			<input type="radio" value='Automatic' name="status" id="r_Auto">Automatic
			<input type="radio" value='Manual' name="status" id="r_Manual">Manual
			<select id='pay_method'></select><br />
		   </div>
		</fieldset>
		<div style='float: left; margin-left: 30%'>
			<button id="button">Change Current Bill</button>
			<button id="button2">Change All Future Bills</button>
		</div>
	</form>
</body>
