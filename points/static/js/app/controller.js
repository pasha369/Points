app.controller('mainCtrl', function($scope, $location, authService) {
    $scope.user = null;

    $scope.initMain = function() {
        $scope.$on('$routeChangeStart', function(next, current) {
            authService.getUser().then(function() {
                $scope.user = authService.user;
                if ($scope.user.id == null) {
                    $location.path('login');
                }
            });
        });
    }

    $scope.isAuth = function() {
        if (user != null) {
            return authService.isAuth;
        } else {
            $location.path('login');
        }
    }

    $scope.logout = function() {
        authService.logout();
    }
});

app.controller('pointCtrl', function($scope, tripService, pointService, routeService, messageFactory, $routeParams, $location, $anchorScroll) {
    $scope.isMain = true;
    $scope.places = [];
    $scope.routeList = [];
    $scope.categories = [];

    $scope.point = { country: null, category: null, };
    $scope.photo;

    $scope.searchText = '';
    $scope.placeId = $routeParams.placeId;
    $scope.likeCount = 0;
    $scope.comments = [];
    $scope.comment = {
        text: '',
        place: $routeParams.placeId
    };

    $scope.currentPlace = {};
    $scope.countries = [];
    $scope.country = {};

    $scope.currentPage = 0;
    $scope.numPerPage = 6;
    $scope.page = [];
    $scope.maxSize = 3;
    $scope.firstItemId = 1;
    $scope.lastItemId = 6;

    $scope.initTripTable = function() {
        tripService.getByUser().then(function(response) {
            $scope.trips = response.data['trips'];
        });
    }

    $scope.discardTrip = function(tripId) {
        tripService.discard(tripId).then(function(response){
            $.each($scope.trips, function(key, trip){
                if(trip.tripId == tripId){
                    $scope.trips.splice(key, 1);
                }
            })
        });
    }

    $scope.nextPage = function() {
        if ($scope.currentPage + 1 < ($scope.maxSize % $scope.numPerPage) && $scope.lastItemId < $scope.maxSize) {
            $scope.currentPage++;
            $scope.firstItemId = ($scope.currentPage * $scope.numPerPage) + 1;
            $scope.lastItemId = (($scope.currentPage + 1) * $scope.numPerPage);
            $scope.page = $scope.places.slice($scope.firstItemId - 1,
                $scope.lastItemId - 1);
        } else if ($scope.lastItemId < $scope.maxSize) {
            $scope.currentPage++;
            $scope.firstItemId = ($scope.currentPage * $scope.numPerPage);
            $scope.lastItemId = $scope.maxSize;
            $scope.page = $scope.places.slice($scope.firstItemId,
                $scope.lastItemId);
        }
    }

    $scope.prevPage = function() {
        if ($scope.currentPage - 1 >= 0) {
            $scope.currentPage--;
            $scope.firstItemId = ($scope.currentPage * $scope.numPerPage) + 1;
            $scope.lastItemId = (($scope.currentPage + 1) * $scope.numPerPage);
            $scope.page = $scope.places.slice($scope.firstItemId - 1,
                $scope.lastItemId - 1);
        }
    }

    function getPage() {
        $scope.page = $scope.places.slice($scope.currentPage * $scope.numPerPage,
            ($scope.currentPage + 1) * $scope.numPerPage);
        $scope.maxSize = $scope.places.length;
        $scope.firstItemId = ($scope.currentPage * $scope.numPerPage) + 1;
        $scope.lastItemId = (($scope.currentPage + 1) * $scope.numPerPage);
        if ($scope.lastItemId > $scope.maxSize) {
            $scope.lastItemId = $scope.maxSize;
        }
    }

    $scope.initGrid = function() {
        $("#select-rate").select2({ minimumResultsForSearch: Infinity });
        pointService.countryList().then(function(response) {
            $scope.countries = response.data;
            $("#select-country").select2({ tags: true });
        })
        pointService.categoryList().then(function(responce) {
            $scope.categories = responce.data;
            $("#select5").select2();
        });

        pointService.placeList().then(function(responce) {
            $scope.places = responce.data['places'];
            getPage();
        })
    }

    $scope.initPlaceForm = function() {
        $("#photo").on("change", function() {
            var formData = new FormData();
            formData.append('photo', this.files[0]);
            pointService.savePhoto(formData).then(function(response) {
                $scope.point.photo = response.data.path;
            });
        });

        pointService.countryList().then(function(response) {
            $scope.countries = response.data;
            $("#select-point-country").select2();
        })

        pointService.categoryList().then(function(responce) {
            $scope.categories = responce.data;
            $("#select5").select2();
        });
        initMap();
    }

    function initMap() {
        var defaultCoord = {
            lat: -34.397,
            lng: 150.644
        };

        var map = new google.maps.Map(document.getElementById('map'), {
            center: defaultCoord,
            scrollwheel: false,
            zoom: 8
        });

        var marker = new google.maps.Marker({
            position: defaultCoord,
            map: map
        });

        google.maps.event.addListener(map, "rightclick", function(event) {
            var lat = event.latLng.lat();
            var lng = event.latLng.lng();
            // populate yor box/field with lat, lng
            $scope.point.latitude = lat;
            $scope.point.langtitude = lng;

            marker.setPosition(new google.maps.LatLng(lat, lng));
            $scope.$apply()
        });

    }

    $scope.initProfile = function() {
        $('.nav-tabs a').click(function(e) {
            e.preventDefault();
            $(this).tab('show');
        });

        pointService.placeByUser().then(function(response) {
            $scope.userPlaces = response.data['places']
        });

        routeService.routeList().then(function(response) {
            $scope.routeList = response.data['routes']
        });
    }

    $scope.initPlaceDetail = function() {
        pointService.placeDetail($scope.placeId).then(function(response) {
            $scope.currentPlace = response.data;

            var defaultCoord = {
                lat: $scope.currentPlace.latitude,
                lng: $scope.currentPlace.langtitude
            };

            var map = new google.maps.Map(document.getElementById('placeMap'), {
                center: defaultCoord,
                scrollwheel: false,
                zoom: 8
            });

            var marker = new google.maps.Marker({
                position: {
                    lat: $scope.currentPlace.latitude,
                    lng: $scope.currentPlace.langtitude
                },
                map: map
            });
        });
    }

    $scope.follow = function(authorId) {
        pointService.follow(authorId);
    }

    $scope.getPlaceByCategory = function(categoryId) {
        pointService.categoryPlaces(categoryId).then(function(responce) {
            $scope.places = responce.data['places'];
            getPage();
        });
    }

    $scope.initCategories = function() {
        pointService.categoryList().then(function(responce) {
            $scope.categories = responce.data;
        });
    }

    $scope.initDropDown = function() {

        $(".be-drop-down").on("click", function() {
            $(this).toggleClass("be-dropdown-active");
            $(this).find(".drop-down-list").stop().slideToggle();
        });
        $(".drop-down-list li").on("click", function() {
            var new_value = $(this).find("a").text();
            $(this).parent().parent().find(".be-dropdown-content").text(new_value);
            return false;
        });
    }

    $scope.search = function(text) {
        if (text) {
            pointService.search(text).then(function(responce) {
                $scope.places = responce.data['places'];

                getPage();
            });
        } else {
            $scope.getPlacePage()
        }
    }

    $scope.getPlacePage = function(pageId) {
        pageId = typeof pageId != 'undefined' ? pageId : 0;
        pointService.placePage(pageId).then(function(responce) {
            $scope.places = responce.data;
        });
    }

    $scope.placeLike = function(placeId) {
        pointService.placeLike(placeId);
    }

    $scope.getLikeCount = function(placeId) {
        pointService.likeCount(placeId).then(function(response) {
            $scope.likeCount = response.data['like_count'];
        });
    }

    $scope.add_comment = function(comment) {
        messageFactory.addComment(comment);
    }

    $scope.get_comments = function() {
        var placeId = $routeParams.placeId;
        messageFactory.getCommentByPlace(placeId).then(function(responce) {
            $scope.comments = responce.data;
        });
    }

    $scope.save = function() {
        $scope.$broadcast('show-errors-check-validity');
        if (!$scope.pointForm.$invalid) {
            pointService.add($scope.point);
            $location.path('profile');
        }
    }

    $scope.remove = function(placeId) {
        pointService.removePlace(placeId).then(function(response) {
            $.each($scope.userPlaces, function(index, item) {
                if (item.id == placeId) {
                    $scope.userPlaces.splice(index, 1);
                    toastr.success(item.title + ' was removed');
                }
            });
        });
    }

    $scope.range = function(n) {
        return new Array(n);
    };

    $scope.scrollTo = function(id) {
        $location.hash(id);
        $anchorScroll();
    }

    $scope.getPlaces = function() {
        pointService.placeList().then(function(responce) {
            $scope.places = responce.data['places'];
            getPage();
        })
    }

    $scope.removeRoute = function(route) {
        routeService.removeRoute(route).then(function(response) {
            $.each($scope.routeList, function(index, item) {
                if (item.id == route) {
                    $scope.routeList.splice(index, 1);
                    toastr.success(item.name + ' was removed');
                }
            });
        });
    }
})

app.controller('authController', function($scope, authService) {
    $scope.credentials = {};
    $scope.user = {};
    $scope.editableUser = {};
    $scope.initSignUp = function() {}

    $scope.signUp = function(user) {
        authService.register(user);
    }

    $scope.sign_in = function(credentials) {
        authService.login(credentials);
    }

    $scope.editProfile = function(editableUser) {
        authService.edit(editableUser);
    }

    $scope.intiEdit = function() {
        authService.getUser().then(function() {
            $scope.user = authService.user;
            if ($scope.user.id == null) {
                $location.path('login');
            }
        });
    }
});

app.controller('dateModalCtrl', function($routeParams, $scope, $uibModal, tripService,  $uibModalInstance) {
    $scope.inlineOptions = {
        customClass: getDayClass,
        minDate: new Date(),
        showWeeks: true
    };

    $scope.dateOptions = {
        formatYear: 'yy',
        maxDate: new Date(2020, 5, 22),
        minDate: new Date(),
        startingDay: 1
    };

    $scope.events = [];
    $scope.openTo = function() {
        $scope.popupTo.opened = true;
    };

    $scope.openFrom = function() {
        $scope.popupFrom.opened = true;
    };

    function getDayClass(data) {
        var date = data.date,
            mode = data.mode;
        if (mode === 'day') {
            var dayToCheck = new Date(date).setHours(0, 0, 0, 0);

            for (var i = 0; i < $scope.events.length; i++) {
                var currentDay = new Date($scope.events[i].date).setHours(0, 0, 0, 0);

                if (dayToCheck === currentDay) {
                    return $scope.events[i].status;
                }
            }
        }
        return '';
    }

    $scope.toggleMin = function() {
        $scope.inlineOptions.minDate = $scope.inlineOptions.minDate ? null : new Date();
        $scope.dateOptions.minDate = $scope.inlineOptions.minDate;
    };

    $scope.popupFrom = {
        opened: false
    };

    $scope.popupTo = {
        opened: false
    };

    $scope.go = function() {
        $uibModalInstance.close({ To: $scope.dtTo, From: $scope.dtFrom });
    };

    $scope.initDateList = function () {
        tripService.getTripDate($routeParams.routeId).then(function(response){
            $scope.trips = response.data['trips'];
        })
    }

    $scope.subscribeTrip = function(tripId){
        tripService.subscribe(tripId);
    }
})

app.controller('routeCtrl', function($scope, pointService, routeService, tripService, messageFactory, $routeParams, $location, $anchorScroll, $uibModal) {

    var map;
    var directionsDisplay = new google.maps.DirectionsRenderer();
    var directionsService = new google.maps.DirectionsService();
    $scope.route = { name: '', selectedPlaces: [] };
    $scope.routes = [];
    $scope.places = [];
    $scope.selectFrom = {};
    $scope.selectTo = {};

    $scope.totalItems = 0;
    $scope.currentPage = 1;
    $scope.maxSize = 5;




    // TODO: Pretiffy this
    $scope.initRouteList = function() {
        routeService.routeList().then(function(response) {
            $scope.routes = response.data['routes']
            $scope.totalItems = $scope.routes.length;
            $scope.routeList = $scope.routes.slice(0, ($scope.currentPage) * 5);
        });
    }

    $scope.openDateList = function() {

        var modalDateInstance = $uibModal.open({
            animation: $scope.animationsEnabled,
            templateUrl: 'static/js/app/views/templates/trip-datelist-modal.html',
            controller: 'dateModalCtrl',
        });

    };

    $scope.open = function() {

        var modalDateInstance = $uibModal.open({
            animation: $scope.animationsEnabled,
            templateUrl: 'static/js/app/views/templates/trip-date-modal.html',
            controller: 'dateModalCtrl',
        });

        modalDateInstance.result.then(function(date) {
            tripService.createTrip($routeParams.routeId, date.From, date.To);
        });
    };

    $scope.pageChanged = function() {
        $scope.routeList = $scope.routes.slice(($scope.currentPage - 1) * 5, $scope.currentPage * 5);
    };

    $scope.calcRoute = function() {
        directionsDisplay.setMap(map);
        directionsDisplay.setOptions({ suppressMarkers: true });
        var lat = $scope.selectFrom.latitude;
        var lng = $scope.selectFrom.langtitude;

        var lat2 = $scope.selectTo.latitude;
        var lng2 = $scope.selectTo.langtitude;

        var request = {
            origin: { lat: lat, lng: lng },
            destination: { lat: lat2, lng: lng2 },
            travelMode: google.maps.TravelMode.DRIVING
        };
        directionsService.route(request, function(result, status) {
            if (status == google.maps.DirectionsStatus.OK) {
                directionsDisplay.setDirections(result);
            }
        });
    }

    function initMap() {
        var defaultCoord = {
            lat: $scope.route.places[0].latitude,
            lng: $scope.route.places[0].langtitude
        };

        map = new google.maps.Map(document.getElementById('routeMap'), {
            center: defaultCoord,
            scrollwheel: false,
            zoom: 8
        });
        $.each($scope.route.places, function(k, place) {
            var marker = new google.maps.Marker({
                position: {
                    lat: place.latitude,
                    lng: place.langtitude
                },
                map: map
            });
            google.maps.event.addListener(marker, 'click', function() {
                marker.info.open(map, marker);
            });
            var content = '<div id="iw-container">' +
                '<div class="iw-title">' + place.title + '</div>' +
                '<div class="row">' +
                '<img src="' + place.photo + '" class="img-responsive col-xs-5">' +
                '<p class="col-xs-7">' + place.description + '</p>' +
                '</div>' +
                '<div class="iw-bottom-gradient"></div>' +
                '</div>';
            marker.info = new google.maps.InfoWindow({
                content: content,
                maxWidth: 350
            });

            google.maps.event.addListener(marker.info, 'domready', function() {

                // Reference to the DIV that wraps the bottom of infowindow
                var iwOuter = $('.gm-style-iw');

                /* Since this div is in a position prior to .gm-div style-iw.
                 * We use jQuery and create a iwBackground variable,
                 * and took advantage of the existing reference .gm-style-iw for the previous div with .prev().
                 */
                var iwBackground = iwOuter.prev();

                // Removes background shadow DIV
                iwBackground.children(':nth-child(2)').css({ 'display': 'none' });

                // Removes white background DIV
                iwBackground.children(':nth-child(4)').css({ 'display': 'none' });

                // Moves the infowindow 115px to the right.
                iwOuter.parent().parent().css({ left: '115px' });

                // Moves the shadow of the arrow 76px to the left margin.
                iwBackground.children(':nth-child(1)').attr('style', function(i, s) {
                    return s + 'left: 76px !important;'
                });

                // Moves the arrow 76px to the left margin.
                iwBackground.children(':nth-child(3)').attr('style', function(i, s) {
                    return s + 'left: 76px !important;'
                });

                // Changes the desired tail shadow color.
                iwBackground.children(':nth-child(3)').find('div').children().css({ 'box-shadow': 'rgba(72, 181, 233, 0.6) 0px 1px 6px', 'z-index': '1' });

                // Reference to the div that groups the close button elements.
                var iwCloseBtn = iwOuter.next();

                // Apply the desired effect to the close button
                iwCloseBtn.css({ opacity: '1', right: '38px', top: '3px', border: '7px solid #48b5e9', 'border-radius': '13px', 'box-shadow': '0 0 5px #3990B9' });

                // If the content of infowindow not exceed the set maximum height, then the gradient is removed.
                if ($('.iw-content').height() < 140) {
                    $('.iw-bottom-gradient').css({ display: 'none' });
                }

                // The API automatically applies 0.7 opacity to the button after the mouseout event. This function reverses this event to the desired value.
                iwCloseBtn.mouseout(function() {
                    $(this).css({ opacity: '1' });
                });
            });

        });
    }

    $scope.initRouteForm = function() {
        pointService.placeList().then(function(response) {
            $scope.places = response.data['places'];
        });
    }

    $scope.initRouteDetail = function() {
        var routeId = $routeParams.routeId;
        routeService.routeDetail(routeId).then(function(response) {
            $scope.route = response.data['route'];
            initMap();
        });
        $('#selectFrom').select2();
        $('#selectTo').select2();
    }

    $scope.saveRoute = function(route) {
        routeService.saveRoute(route);
    }

    $scope.removeRoute = function(route) {
        routeService.removeRoute(route);
    }

    $scope.selectPlace = function(place) {
        $scope.route.selectedPlaces.push(place);
    }

    $scope.deselectPlace = function(place) {
        var selectId = $scope.route.selectedPlaces.indexOf(place);
        $scope.route.selectedPlaces.splice(selectId, 1);
    }

    $scope.searchPlace = function() {

    }

});