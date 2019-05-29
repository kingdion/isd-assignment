
$(document).ready(function(){
    $('#createuser-form').submit(function(event) {
        event.preventDefault();

        if (validate_form()) {
            $('#submit-btn').attr('disabled', true);

            $.post($(this).attr('action'), $(this).serialize(), createuser_callback);
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


function createuser_callback(data) {
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
        alert("User has been successfully created!");
	location.reload();
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

function validate_email() {
    var email = $('[name=email]');
    if (email.val().length == 0) {
        set_warning(email, 'Required field.');
        return false;
    }
    else {
        clear_warning(email);
        return true;
    }
}

function validate_password() {
    var pword = $('[name=password]');
    var pword_check = check_password(pword.val());
    if (!pword_check.success) {
        set_warning(pword, pword_check.warning);
        return false;
    }
    else {
        clear_warning(pword);
        return true;
    }
}

function validate_repeat_password() {
    var repeat_pword = $('[name=repeat-password]');
    if (repeat_pword.val().length == 0) {
        set_warning(repeat_pword, 'Required field.');
        return false;
    }
    else if (repeat_pword.val() != $('[name=password]').val()) {
        set_warning(repeat_pword, 'Passwords do not match.');
        return false;
    }
    else {
        clear_warning(repeat_pword);
        return true;
    }
}

function validate_fname() {
    var fname = $('[name=first-name]');
    if (fname.val().length == 0) {
        set_warning(fname, 'Required field.');
        return false;
    }
    else {
        clear_warning(fname);
        return true;
    }
}

function validate_lname() {
    var lname = $('[name=last-name]');
    if (lname.val().length == 0) {
        set_warning(lname, 'Required field.');
        return false;
    }
    else {
        clear_warning(lname);
        return true;
    }
}

function validate_street() {
    var street = $('[name=street-address]');
    if (street.val().length == 0) {
        set_warning(street, 'Required field.');
        return false;
    }
    else {
        clear_warning(street);
        return true;
    }
}

function validate_postcode() {
    var postcode = $('[name=postcode]');
    if (postcode.val().length == 0) {
        set_warning(postcode, 'Required field.');
        return false;
    }
    else {
        clear_warning(postcode);
        return true;
    }
}

function validate_phone() {
    var phone = $('[name=phone-number]');
    if (phone.val().length == 0) {
        set_warning(phone, 'Required field.');
        return false;
    }
    else {
        clear_warning(phone);
        return true;
    }
}

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

function check_password(pword) {
    var result = { 'success': true, 'warning': '' };

    if (pword.length < 8) {
        result.success = false;
        result.warning += 'Must be at least 8 characters long.';
    }

    if (pword.includes(' ')) {
        result.success = false;
        if (result.warning.length > 0) result.warning += '\n';
        result.warning += 'Cannot contain any spaces.';
    }

    if (!pword.match(/[^\w ]/)) {
        result.success = false;
        if (result.warning.length > 0) result.warning += '\n';
        result.warning += 'Must contain at least 1 special character.';
    }

    return result;
}

