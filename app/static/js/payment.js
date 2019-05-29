$(document).ready(function(){
    $('#payment-form').submit(function(event) {
        event.preventDefault();

        if (validate_form()) {
            $('#submit-btn').attr('disabled', true);

            $.post($(this).attr('action'), $(this).serialize(), payment_callback);
        }
  });

  $('[name=email]').focusout(validate_email);
  $('[name=password]').focusout(function () {
      validate_password();
      validate_repeat_password();
  });
  $('[name=repeat-password]').focusout(function () {
      validate_repeat_password();
      validate_password();
  });
  $('[name=first-name]').focusout(validate_fname);
  $('[name=last-name]').focusout(validate_lname);
  $('[name=street-address]').focusout(validate_street);
  $('[name=postcode]').focusout(validate_postcode);
  $('[name=phone-number]').focusout(validate_phone);
});

function payment_callback(data) {
    console.log(data); //debugging
    if (!data.success) {
        if (data.reason == 'email exists') {
            set_warning($('[name=email]'), 'A user with this email already exists.');
            $('#submit-btn').attr('disabled', false);
        }
        else {
            alert("Error, failed to create account: " + data.reason);
        }
    }
    else {
        window.location.href = "/dashboard"
    }
}

function validate_form() {
    return !(
             !validate_email()
              | !validate_password()
              | !validate_repeat_password()
              | !validate_fname()
              | !validate_lname()
              | !validate_street()
              | !validate_postcode()
              | !validate_phone()
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
    var daddress = $('[name=dstreet-address]');
    if (daddress.val().length == 0) {
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
        result.warning += 'Must be at least 16 characters long.';
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
    if (billpostcodet.val().length == 0) {
        set_warning(billpostcode, 'Required field.');
        return false;
    }
    else {
        clear_warning(billpostcode);
        return true;
    }
}

