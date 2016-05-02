app.factory('pointService', function($http) {
    return {
        add: function(place) {
            $http({
                method: 'POST',
                url: 'api/points/add/',
                data: {
                    place: place,
                },
                dataType: 'json',
            }).then(function successCallback(response) {
                toastr.success('success');
            })
        },

        removePlace: function(placeId) {
            return $http({
                method: 'POST',
                url: 'api/points/remove/',
                data: { place_id: placeId }
            });
        },

        savePhoto: function(formData) {
            return $http({
                method: 'POST',
                url: 'api/points/saveplacephoto/',
                data: formData,
                headers: {
                    'Content-Type': undefined
                },
                transformRequest: angular.identity
            });
        },

        placePage: function(page_id) {
            return $http({
                method: 'POST',
                url: 'api/points/get_place_page/',
                data: { page_id: page_id }
            })
        },

        placeDetail: function(placeId) {
            return $http({
                method: 'POST',
                url: 'api/points/place-detail/',
                data: { place_id: placeId }
            })
        },

        placeByUser: function() {
            return $http({
                method: 'POST',
                url: 'api/points/get-by-user/',
            });
        },

        placeList: function() {
            return $http({
                method: 'GET',
                url: 'api/points/place-list',
                dataType: 'json',
            });
        },

        placeLike: function(placeId) {
            $http({
                method: 'POST',
                url: 'api/points/place_like/',
                data: { place: placeId }
            });
        },

        likeCount: function(placeId) {
            return $http({
                method: 'POST',
                url: 'api/points/get_place_likes/',
                data: { place_id: placeId }
            });
        },

        getFavorite: function() {
            return $http({
                method: 'POST',
                url: 'api/points/get-favorite/'
            });
        },

        removeFavorite: function(placeId) {
            return $http({
                method: 'POST',
                url: 'api/points/remove-favorite/',
                data: {placeId: placeId}
            });
        },

        search: function(text) {
            return $http({
                method: 'POST',
                url: 'api/points/search/',
                data: { search_text: text }
            })
        },

        categoryList: function() {
            return $http({
                method: 'POST',
                url: 'api/points/category-list/'
            });
        },

        categoryPlaces: function(categoryId) {
            return $http({
                method: 'POST',
                url: 'api/points/category-places/',
                data: { category_id: categoryId }
            });
        },

        follow: function(personId) {
            return $http({
                method: 'POST',
                url: 'api/login/follow',
                data: { person: personId }
            });
        },

        countryList: function() {
            return $http({
                method: 'POST',
                url: 'api/points/country-list/',
            });
        }
    }
});

app.factory('authService', function($http, $location) {
    return {
        user: {},
        isAuth: false,
        login: function(credentials) {
            var self = this;
            $http({
                method: 'POST',
                url: 'api/login/sign_in',
                data: credentials,
                dataType: 'json',
            }).then(function(response) {
                self.user = response.data['user'];
                self.isAuth = true;
                $location.path('/profile')
                    //toastr.success( self.user.first_name + " log in.");
            });
        },

        register: function(user) {
            $http({
                method: 'POST',
                url: 'api/login/sign_up',
                data: { user: user },
            }).then(function(response) {
                toastr.success("user register");
                user = response.data['user'];
                self.isAuth = true;
                $location.path('/profile')
            });
        },

        getUser: function() {
            var self = this;
            return $http({
                method: 'POST',
                url: 'api/login/get-user',
            }).then(function(response) {
                self.user = response.data['user'];
            })
        },

        logout: function() {
            var self = this;
            $http({
                method: 'POST',
                url: 'api/login/logout',
            }).then(function() {
                self.user = null;
                $location.path('/login');
            })
        },

        edit: function(editableUser) {
            return $http.post('api/login/edit', { user_data: editableUser });
        },

        isAuthenticated: function() {
            // TODO: if not redirect to login
        }
    }
});

app.factory('routeService', function($http) {
    return {
        saveRoute: function(route) {
            return $http({
                method: 'POST',
                url: 'api/points/save-route/',
                data: { route: route }
            });
        },

        routeDetail: function(routeId) {
            return $http({
                method: 'POST',
                url: 'api/points/route-detail/',
                data: { routeId: routeId }
            })
        },

        removeRoute: function(routeId) {
            return $http({
                method: 'POST',
                url: 'api/points/remove-route/',
                data: { routeId: routeId }
            });
        },

        routeList: function() {
            return $http({
                method: 'POST',
                url: 'api/points/route-list/',
            });
        }
    }
});

app.factory('tripService', function($http) {
    return {
        createTrip: function(routeId, dateFrom, dateTo) {
            $http({
                method: 'POST',
                url: 'api/points/add-trip/',
                data: {
                    routeId: routeId,
                    dateFrom: dateFrom,
                    dateTo: dateTo
                }
            });
        },

        getByUser: function() {
            return $http({
                method: 'POST',
                url: 'api/points/trip-by-user/',
            });
        },

        getTripDate: function(tripId) {
            return $http({
                method: 'POST',
                url: 'api/points/trip-date/',
                data: {tripId: tripId}
            });
        },

        getAll: function() {
            return $http({
                method: 'POST',
                url: 'api/points/get-all/',
            });
        },

        subscribe: function(tripId) {
            $http({
                method: 'POST',
                url: 'api/points/subscribe-trip/',
                data: { tripId: tripId }
            });
        },

        discard: function(tripId) {
            return $http({
                method: 'POST',
                url: 'api/points/discard-trip/',
                data: { tripId: tripId }
            });
        },
    }
});

app.factory('messageFactory', function($http) {
    return {
        addComment: function(comment) {
            return $http({
                method: 'POST',
                url: 'api/message/add/',
                data: { comment: comment }
            });
        },
        getCommentByPlace: function(placeId) {
            return $http({
                method: 'POST',
                url: 'api/message/get_by_place/',
                data: { place_id: placeId },
                dataType: 'json'
            })
        }
    }
})