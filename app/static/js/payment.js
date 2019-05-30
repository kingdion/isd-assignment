$(document).ready(function(){
    $('#payment-form').submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: $('#payment-form').attr('action'),
            data: {dfirst : $("[name=dfirst]").val(), dlast : $("[name=dlast]").val(), daddress : $("[name=daddress]").val(), dpostcode : $("[name=dpostcode]").val(), cname : $("[name=cname]").val(), credit_no : $("[name=credit-no]").val(), cvc : $("[name=cvc]").val(), month : $("[name=month]").val(), year : $("[name=year]").val(), bfirst_name : $("[name=bfirst-name]").val(), blast_name : $("[name=blast-name]").val(), bstreet_address : $("[name=bstreet-address]").val(), bpostcode : $("[name=bpostcode]").val()},
            success: (data) => 
            { 
                if (data.success) 
                { 
                    window.location.href = "/browse" 
                    var myObj = { firsname : "John", lastname : "Doe" };
                    console.log(myObj);
                } 
                else 
                { 
                    window.location.href = "/login"
                    var myObj = { firsname : "No", lastname : "work" };
                    console.log(myObj);
                }
            },
          });

        if (validate_form()) {
            
            $.post($(this).attr('action'), $(this).serialize());
        }
        
  });

  //when clicking off an input, calls focusout
  $('[name=dfirst]').focusout(validate_dfirst);
  $('[name=dlast]').focusout(validate_dlast);
  $('[name=daddress]').focusout(validate_daddress);
  $('[name=dpostcode]').focusout(validate_dpostcode);
  $('[name=cname]').focusout(validate_creditname);
  $('[name=credit-no]').focusout(validate_creditno);
  $('[name=cvc]').focusout(validate_cvc);
  $('[name=month]').focusout(validate_month);
  $('[name=year]').focusout(validate_year); 
  $('[name=bfirst-name]').focusout(validate_bfirst);
  $('[name=blast-name]').focusout(validate_blast);
  $('[name=bstreet-address]').focusout(validate_billaddress);
  $('[name=bpostcode]').focusout(validate_billpostcode);

});

function validate_form() {
    return !(
        !validate_dfirst()
        | !validate_dlast()
        | !validate_daddress()
        | !validate_dpostcode()
        | !validate_creditname()
        | !validate_creditno()
        | !validate_cvc()
        | !validate_month()
        | !validate_year()
        | !validate_bfirst()
        | !validate_blast()
        | !validate_billaddress()
        | !validate_billpostcode()
            );
}

//delivery form validation

function validate_dfirst() {
    var dfirst = $('[name=dfirst]');
    if (dfirst.val().length == 0) {
        set_warning(dfirst, 'Required field.');
            return false;
    }
    else {
        clear_warning(dfirst);
        return true;
    }
}
function validate_dlast() {
    var dlast = $('[name=dlast]');
    if (dlast.val().length == 0) {
        set_warning(dlast, 'Required field.');
        return false;
    }
    else {
        clear_warning(dlast);
        return true;
    }
}

function validate_daddress() {
    var dadd = $('[name=daddress]');
    if (dadd.val().length == 0) {
        set_warning(daddress, 'Required field.');
        return false;
    }
    else {
        clear_warning(daddress);
        return true;
    }
}


function validate_dpostcode() {
    var dpost = $('[name=dpostcode]');
    if (dpost.val().length == 0) {
        set_warning(dpost, 'Required field.');
        return false;
    }
    else {
        clear_warning(dpost);
        return true;
    }
}

//credit card form validation
function validate_creditname() {
    var creditname = $('[name=cname]');
    if (creditname.val().length == 0) {
        set_warning(creditname, 'Required field.');
        return false;
    }
    else {
        clear_warning(creditname);
        return true;
    }
}

function validate_creditno() {
    var creditno = $('[name=credit-no]');
    var creditcheck = check_creditcard(creditno.val());
    if (!creditcheck.success) {
        set_warning(creditno, creditcheck.warning);
        return false;
    }
    else {
        clear_warning(creditno);
        return true;
    }
}

function check_creditcard(creditno) {
    var result = { 'success': true, 'warning': '' };

    if (creditno.length < 16) {
        result.success = false;
        result.warning += 'Must be at least 16 numbers long.';
    }
    return result;
}


function validate_cvc() {
    var cvcno = $('[name=cvc]');
    var cvccheck = check_cvc(cvcno.val());
    if (!cvccheck.success) {
        set_warning(cvcno, cvccheck.warning);
        return false;
    }
    else {
        clear_warning(cvcno);
        return true;
    }
}

function check_cvc(cvcno) {
    var result = { 'success': true, 'warning': '' };

    if (cvcno.length < 3) {
        result.success = false;
        result.warning += 'CVC must be at least 3 characters long.';
    }
    return result;
}

function validate_month() {
    var creditmonth = $('[name=month]');
    if (creditmonth.val().length == 0) {
        set_warning(creditmonth, 'Required field.');
        return false;
    }
    else {
        clear_warning(creditmonth);
        return true;
    }
}

function validate_year() {
    var credityear = $('[name=year]');
    if (credityear.val().length == 0) {
        set_warning(credityear, 'Required field.');
        return false;
    }
    else {
        clear_warning(credityear);
        return true;
    }
}

//warnings for credit card checks
function set_warning(el, warning) {
    el.tooltip('hide')
      .css('border', '1px solid red')
      .prop('title', warning)
      .attr('data-original-title', warning)
      .tooltip('show');
}

function clear_warning(el) {
    el.css('border', '1px solid #ced4da')
      .prop('title', '')
      .attr('data-original-title', '')
      .tooltip('hide');
}

//billing form validation
function validate_bfirst() {
    var billfirst = $('[name=bfirst-name]');
    if (billfirst.val().length == 0) {
        set_warning(billfirst, 'Required field.');
        return false;
    }
    else {
        clear_warning(billfirst);
        return true;
    }
}

function validate_blast() {
    var billlast = $('[name=blast-name]');
    if (billlast.val().length == 0) {
        set_warning(billlast, 'Required field.');
        return false;
    }
    else {
        clear_warning(billlast);
        return true;
    }
}

function validate_billaddress() {
    var billaddress = $('[name=bstreet-address]');
    if (billaddress.val().length == 0) {
        set_warning(billaddress, 'Required field.');
        return false;
    }
    else {
        clear_warning(billaddress);
        return true;
    }
}

function validate_billpostcode() {
    var billpostcode = $('[name=bpostcode]');
    var bpostcheck = check_bpost(billpostcode.val());
    if (!bpostcheck.success) {
        set_warning(billpostcode, bpostcheck.warning);
        return false;
    }
    else {
        clear_warning(billpostcode);
        return true;
    }
}

function check_bpost(billpostcode) {
    var result = { 'success': true, 'warning': '' };

    if (billpostcode.length < 4) {
        result.success = false;
        result.warning += 'Postcode must be at least 4 numbers long.';
    }
    return result;
}
