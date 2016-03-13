app.directive('placePost', function() {
    return {
        restrict: 'E',
        scope: {
            place: '=place',
            isEdit: '=',
            remove: '&remove'
        },
        templateUrl: 'static/js/app/views/directives/place-post.html'
    };
});

app.directive('placeMiniature', function() {
    return {
        restrict: 'E',
        scope: {
            place: '=place',
        },
        templateUrl: 'static/js/app/views/directives/place-miniature.html'
    };
});

app.directive('routeMiniature', function() {
    return {
        restrict: 'E',
        scope: {
            isEdit: '=',
            route: '=route',
            remove: '&remove'
        },
        templateUrl: 'static/js/app/views/directives/route-miniature.html'
    };
});

app.directive('showErrors', function() {
    return {
        restrict: 'A',
        require: '^form',
        link: function(scope, el, attrs, formCtrl) {
            // find the text box element, which has the 'name' attribute
            var inputEl = el[0].querySelector("[name]");
            // convert the native text box element to an angular element
            var inputNgEl = angular.element(inputEl);
            // get the name on the text box so we know the property to check
            // on the form controller
            var inputName = inputNgEl.attr('name');

            // only apply the has-error class after the user leaves the text box
            inputNgEl.bind('blur', function() {
                el.toggleClass('has-error', formCtrl[inputName].$invalid);
            });

            scope.$on('show-errors-check-validity', function() {
                el.toggleClass('has-error', formCtrl[inputName].$invalid);
            });
        }
    }
});
