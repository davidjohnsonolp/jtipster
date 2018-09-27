var User = Backbone.Model.extend({
    urlRoot: '/api/user',

    validate: function (attrs) {
        var errors = [];

        if (!attrs.username) {
            errors.push({name: 'username', message: 'Please fill username field.'});
        }
        if (!attrs.password) {
            errors.push({name: 'password', message: 'Please fill password field.'});
        }
        if (!attrs.email) {
            errors.push({name: 'email', message: 'Please fill email field.'});
        }

        return errors.length > 0 ? errors : false;
    }
});

var RegisterView = Backbone.View.extend({
    events: {
        'click button': 'register'
    },

    register: function (e) {
        e.preventDefault();
        this.hideErrors();

        var registrationDetails = {
                username: $('#username-input').val(),
                password: $('#password-input').val(),
                email: $('#email-input').val(),
                recaptcha: grecaptcha.getResponse()
            },
            options = {
                success: function() {
                    alert('Thanks for registering. Please log in to complete registration.');
                    document.location.href = 'login';
                },
                error: function (model, response){
                    switch(response.status) {
                        case 400: return alert('Invalid form entry. Please try again.');
                        case 403: return alert('Please confirm you are not a robot.');
                        case 409: return alert('Username/email already registered. Please try again or click the "Password Reminder" link.');
                        default: return alert('There has been a problem with your request. Please try again.');
                    }
                }
            }

        if (!registrationDetails.recaptcha)
            return alert('Please confirm you are not a robot.');

        if (!this.model.save(registrationDetails, options))
            this.showErrors(this.model.validationError);
    },

    showErrors: function(errors) {
        _.each(errors, function (error) {
            var input = this.$('#' + error.name),
                output = this.$('#' + error.name + ' output');

            input.addClass('error');
            output.text(error.message);
        }, this);
    },

    hideErrors: function () {
        var li = this.$('li'),
            output = this.$('output');

        li.removeClass('error');
        output.text('');
    }
});