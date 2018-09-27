var Authenticate = Backbone.Model.extend({
    url: '/api/authenticate',

    validate: function(attrs){
        var errors = [];

        if (!attrs.username) {
            errors.push({name: 'username', message: 'Please fill username field.'});
        }
        if (!attrs.password) {
            errors.push({name: 'password', message: 'Please fill password field.'});
        }
    }
});

var LoginView = Backbone.View.extend({
    events: {
        'click button': 'login'
    },

    login: function (e) {
        e.preventDefault();
        this.hideErrors();

        var loginDetails = {
                username: $('#username-input').val(),
                password: $('#password-input').val(),
                remember_me: $('#remember_me').is(':checked')
            },
            options = {
                success: function(model, response, options) {
                    // get redirect - qs param = next
                    document.location.href = '/';
                },
                error: function (model, response, options){
                    switch(response.status) {
                        case 400: return alert('Invalid form entry. Please try again.');
                        case 401: return alert('Username/password not recognised. Please try again or click the "Password Reminder" link.');
                        default: return alert('There has been a problem with your request. Please try again.');
                    }
                }
            }

        if (!this.model.save(loginDetails, options))
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