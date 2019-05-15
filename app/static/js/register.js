//console.log('fuck');

$(document).ready(function(){
    $('[name=register-form]').submit(function(event){
        if (!validate_form()) {
            event.preventDefault();
        }
        else {
            return;
        }
  });
});

function validate_form() {
    var no_warnings = true;

    var email = $('[name=email]');
    if (email.val().length == 0) {
        set_warning(email, 'Required field.');
        no_warnings = false;
    }
    else {
        clear_warning(email);
    }

    var pword = $('[name=password]');
    var pword_validation = validate_password(pword.val());
    if (!pword_validation.success) {
        set_warning(pword, pword_validation.warning);
        no_warnings = false;
    }
    else {
        clear_warning(pword);
    }

    var repeat_pword = $('[name=repeat-password]');
    if (repeat_pword.val().length == 0) {
        set_warning(repeat_pword, 'Required field.');
        no_warnings = false;
    }
    else if (repeat_pword.val() != pword.val()) {
        set_warning(repeat_pword, 'Passwords do not match.');
        no_warnings = false;
    }
    else {
        clear_warning(repeat_pword);
    }

    return no_warnings;
}

function set_warning(el, warning) {
    console.log(warning);

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

function validate_password(pword) {
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
