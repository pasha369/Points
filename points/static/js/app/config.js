app.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
        when('/', {
            templateUrl: 'static/js/app/views/pages/home.html',
            controller: 'pointCtrl'
        }).
        when('/login', {
            templateUrl: 'static/js/app/views/pages/sign-in.html',
            controller: 'authController'
        }).
        when('/register', {
            templateUrl: 'static/js/app/views/pages/sign-up.html',
            controller: 'authController'
        }).
        when('/discover', {
            templateUrl: 'static/js/app/views/pages/discover.html',
            controller: 'pointCtrl'
        }).
        when('/profile', {
            templateUrl: 'static/js/app/views/pages/profile.html',
            controller: 'pointCtrl'
        }).
        when('/profile/edit', {
            templateUrl: 'static/js/app/views/pages/profile-edit.html',
            controller: 'pointCtrl'
        }).
        when('/detail/:placeId', {
            templateUrl: 'static/js/app/views/pages/place-detail.html',
            controller: 'pointCtrl'
        }).
        when('/add-place/', {
            templateUrl: 'static/js/app/views/pages/create-place.html',
            controller: 'pointCtrl'
        }).
        when('/add-route/', {
            templateUrl: 'static/js/app/views/pages/create-route.html',
            controller: 'routeCtrl'
        }).
        when('/route-detail/:routeId', {
            templateUrl: 'static/js/app/views/pages/route-detail.html',
            controller: 'routeCtrl'
        }).
        otherwise({
            redirectTo: '/'
        });
    }
]);