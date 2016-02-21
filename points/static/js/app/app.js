var app = angular.module('app', ['ngRoute']);

app.config(function($interpolateProvider, $httpProvider ) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});