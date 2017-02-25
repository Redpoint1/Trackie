(function () {
    "use strict";
    var trackie_module = angular.module("trackie", ["ngRoute", "ngResource", "ngCookies", "ngAnimate", "ngTouch", "restangular", "ui.grid", "ui.grid.selection", "ui.grid.saveState", "ui.grid.pagination", "naif.base64"])
        .constant("CONFIG", {
            "DEBUG": false
        })
        .constant("VARS", {
            "FORBIDDEN_URL": "/forbidden",
            "PARTIALS_REGEX": /partials\/.+/
        })
        .config(["$provide", function ($provide) {
            $provide.decorator("$templateCache", [
                "$delegate", function ($delegate) {

                    var keys = [];
                    var origPut = $delegate.put;
                    var origRemove = $delegate.remove;
                    var origRemoveAll = $delegate.removeAll;

                    $delegate.put = function (key, value) {
                        origPut(key, value);
                        keys.push(key);
                        keys = _.uniq(keys);
                    };

                    $delegate.remove = function (key) {
                        origRemove(key);
                        _.pull(keys, key);
                    };

                    $delegate.removeAll = function () {
                        origRemoveAll();
                        keys = [];
                    };

                    $delegate.getKeys = function () {
                        return keys;
                    };

                    $delegate.removeAllByKey = function (regex) {
                        var keysToDelete = _.filter($delegate.getKeys(), function(n){
                            return regex.test(n);
                        });
                        _.forEach(keysToDelete, function(key){
                            $delegate.remove(key);
                        });
                    };

                    return $delegate;
                }
            ]);
        }])
        .config(["$interpolateProvider", function ($interpolateProvider) {
            // $interpolateProvider.startSymbol("{$");
            // $interpolateProvider.endSymbol("$}");
        }])
        .config(["$resourceProvider", function($resourceProvider) {
            $resourceProvider.defaults.stripTrailingSlashes = false;
        }])
        .config(["$httpProvider", function ($httpProvider) {
            $httpProvider.defaults.xsrfCookieName = "csrftoken";
            $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken";
        }])
        .config(["RestangularProvider", function (RestangularProvider) {
            RestangularProvider.setBaseUrl("/api/v1/trackie");
            RestangularProvider.setFullResponse(true);
            RestangularProvider.setRequestSuffix("/");
        }])
        .config(["$routeProvider", "$locationProvider", "VARS", function ($routeProvider, $locationProvider, VARS) {
            $routeProvider.when("/", {
                templateUrl: "partials/main.html",
                controller: "MainController",
                reloadAfterAuthChange: true
            }).when("/profile", {
                templateUrl: "partials/profile.html",
                controller: "ProfileController",
                reloadAfterAuthChange: true,
                throwAuthError: true
            }).when("/race/:id", {
                templateUrl: "partials/map.html",
                controller: "MapController"
                //reloadAfterAuthChange: true,
            }).when("/track/add", {
                templateUrl: "partials/track/create.html",
                controller: "TrackCreateController",
                reloadAfterAuthChange: true,
                throwAuthError: true
            }).when("/track/:id", {
                templateUrl: "partials/track/detail.html",
                controller: "TrackController",
                reloadAfterAuthChange: true
            }).when("/403", {
                templateUrl: "partials/status/403.html"
            }).when("/404", {
                templateUrl: "partials/status/404.html"
            }).when(VARS.FORBIDDEN_URL, {
                templateUrl: "partials/status/403.html"
            }).otherwise({
                redirectTo: "/404"
            });

            //$locationProvider.html5Mode(true);
        }])
        .run(["$rootScope", "$location", "$route", "djangoAuth", function ($rootScope, $location, $route, djangoAuth) {
            djangoAuth.initialize();
            $rootScope.$on("$routeChangeStart", function (event, toState, toParams) {
                var state = toState.redirectTo ? $route.routes[toState.redirectTo]: toState;
                djangoAuth.authenticationStatus().then(function () {
                    djangoAuth.checkPageAuth(state.throwAuthError);
                });
            });
       }]);

    // Services

    trackie_module.service("djangoAuth", ["$q", "$http", "$cookies", "$rootScope", "$templateCache", "$location", "$routeParams", "$route", "VARS", function ($q, $http, $cookies, $rootScope, $templateCache, $location, $routeParams, $route, VARS) {
        return {
            "API_URL": "api/v1/auth",
            "use_session": true,
            "authenticated": null,
            "authPromise": null,
            "user": null,
            "request": function (args) {
                if ($cookies.token) {
                    $http.defaults.headers.common.Authorization = "Token " + $cookies.token;
                }
                args = args || {};
                var deferred = $q.defer();
                var url = this.API_URL + args.url;
                var method = args.method || "GET";
                var params = args.params || {};
                var data = args.data || {};
                $http({
                    url: url,
                    withCredentials: this.use_session,
                    method: method.toUpperCase(),
                    params: params,
                    headers: {"X-Requested-With": "XMLHttpRequest"},
                    data: data
                }).success(angular.bind(this, function (data, status) {
                    deferred.resolve(data, status);
                })).error(angular.bind(this, function (data, status, headers, config) {
                    if (data) {
                        data.status = status;
                    }
                    if (status === 0) {
                        if (data === "") {
                            data = {};
                            data.status = 0;
                            data.non_field_errors = ["Could not connect. Please try again."];
                        }
                        if (data === null) {
                            data = {};
                            data.status = 0;
                            data.non_field_errors = ["Server timed out. Please try again."];
                        }
                    }
                    deferred.reject(data, status, headers, config);
                }));
                return deferred.promise;
            },
            "register": function (username, password1, password2, email, more) {
                var data = {
                    "username": username,
                    "password1": password1,
                    "password2": password2,
                    "email": email
                };
                data = angular.extend(data, more);
                return this.request({
                    "method": "POST",
                    "url": "/registration/",
                    "data": data
                });
            },
            "login": function (username, password) {
                var djangoAuth = this;
                return this.request({
                    "method": "POST",
                    "url": "/login/",
                    "data": {
                        "username": username,
                        "password": password
                    }
                }).then(function (data) {
                    if (!djangoAuth.use_session) {
                        $http.defaults.headers.common.Authorization = "Token " + data.key;
                        $cookies.token = data.key;
                    }
                    djangoAuth.authenticated = true;
                    djangoAuth.user = data.user;
                    djangoAuth.changedAuth();
                    $rootScope.$broadcast("djangoAuth.logged_in", data);
                });
            },
            "logout": function () {
                var djangoAuth = this;
                return this.request({
                    "method": "POST",
                    "url": "/logout/"
                }).then(function () {
                    delete $http.defaults.headers.common.Authorization;
                    delete $cookies.token;
                    // delete $cookies.sessionid;
                    djangoAuth.authenticated = false;
                    djangoAuth.user = null;
                    djangoAuth.changedAuth();
                    $rootScope.$broadcast("djangoAuth.logged_out");
                });
            },
            "changePassword": function (password1, password2) {
                return this.request({
                    "method": "POST",
                    "url": "/password/change/",
                    "data": {
                        "new_password1": password1,
                        "new_password2": password2
                    }
                });
            },
            "resetPassword": function (email) {
                return this.request({
                    "method": "POST",
                    "url": "/password/reset/",
                    "data": {
                        "email": email
                    }
                });
            },
            "profile": function () {
                return this.request({
                    "method": "GET",
                    "url": "/user/"
                });
            },
            "updateProfile": function (data) {
                return this.request({
                    "method": "PATCH",
                    "url": "/user/",
                    "data": data
                });
            },
            "verify": function (key) {
                return this.request({
                    "method": "POST",
                    "url": "/registration/verify-email/",
                    "data": {"key": key}
                });
            },
            "confirmReset": function (uid, token, password1, password2) {
                return this.request({
                    "method": "POST",
                    "url": "/password/reset/confirm/",
                    "data": {
                        "uid": uid,
                        "token": token,
                        "new_password1": password1,
                        "new_password2": password2
                    }
                });
            },
            "authenticationStatus": function (restrict, force) {
                restrict = restrict || false;
                force = force || false;
                if (this.authPromise === null || force) {
                    this.authPromise = this.profile();
                }
                var self = this;
                var defer = $q.defer();
                if (this.authenticated !== null && !force) {
                    if (this.authenticated === false && restrict) {
                        defer.reject("User is not logged in.");
                    } else {
                        defer.resolve();
                    }
                } else {
                    this.authPromise.then(function (data) {
                        if (!self.authenticated) {
                            $templateCache.removeAllByKey(VARS.PARTIALS_REGEX);
                        }
                        self.authenticated = true;
                        self.user = data;
                        defer.resolve();
                    }, function () {
                        if (self.authenticated) {
                            $templateCache.removeAllByKey(VARS.PARTIALS_REGEX);
                        }
                        self.authenticated = false;
                        self.user = null;
                        if (restrict) {
                            defer.reject("User is not logged in.");
                        } else {
                            defer.resolve();
                        }
                    });
                }
                return defer.promise;
            },
            "changedAuth": function () {
                $templateCache.removeAllByKey(VARS.PARTIALS_REGEX);
                var route = $route.current.redirectTo ? $route.routes[$route.current.redirectTo] : $route.current;
                this.checkPageAuth(route.throwAuthError, route.reloadAfterAuthChange);
            },
            "checkPageAuth": function (throwAuthError, reload) {
                var currentPath = $location.path() || "/";

                if (currentPath !== VARS.FORBIDDEN_URL) {
                    if (throwAuthError && !this.authenticated) {
                        $location.path("/forbidden");
                        $location.search("from", currentPath);
                    } else if (reload) {
                        $route.reload();
                    }
                } else {
                    // TODO refactor 25.02. 2017
                    var from  = $route.current.params.from || "/";
                    // not good for dynamic routes like /tracks/:id
                    var route = $route.routes[from] || {};
                    if (route.throwAuthError){
                        if (this.authenticated) {
                            $location.url(from);
                        }
                    } else {
                        $location.url(from);
                    }
                }
            },
            "initialize": function (url, sessions) {
                this.API_URL = url || this.API_URL;
                this.use_session = sessions || this.use_session;
                return this.authenticationStatus();
            }
        };
    }]);

    // Directives

    trackie_module.directive("loginModal", ["djangoAuth", "$window", function (djangoAuth, $window) {
        function link(scope, element) {
            scope.djangoAuth = djangoAuth;
            scope.login = function (username, password) {
                djangoAuth.login(username, password).then(function () {
                    element.find("#login-modal").removeClass("in").hide();
                    element.find("#login-modal-backdrop").fadeOut().removeClass("in");
                }, function (error) {
                    renderFormErrors(element.find("form"), error);
                });
            };
            scope.logout = function () {
                djangoAuth.logout().then(function () {
                    //TODO: todo (todoception)
                }, function () {
                    $window.alert("Nedá sa odhlásiť. Skúste to neskôr.");
                });
            };
        }

        return {
            link: link,
            restrict: "AE",
            templateUrl: "partials/login.html",
            scope: {}
        };
    }]);

    trackie_module.directive("sameValueAs", [function () {
        function link(scope, elem, attrs, ctrl) {
            var secondField = elem.parents("form").find("#" + attrs.sameValueAs);

            elem.on("keyup", function () {
                scope.$apply(function () {
                    var ngField = ctrl.$$parentForm[secondField.attr("name")];
                    var isValid = (ctrl.$pristine || ngField.$pristine) ? true : elem.val() === secondField.val();
                    ctrl.$setValidity("sameValue", isValid);
                    ngField.$setValidity("sameValue", isValid);
                });
            });

            secondField.on("keyup", function () {
                scope.$apply(function () {
                    var ngField = ctrl.$$parentForm[secondField.attr("name")];
                    var isValid = (ctrl.$pristine || ngField.$pristine) ? true : elem.val() === secondField.val()
                    ctrl.$setValidity("sameValue", isValid);
                    ngField.$setValidity("sameValue", isValid);
                });
            });
        }

        return {
            require: "ngModel",
            link: link
        };
    }]);

    trackie_module.directive("validFile", function () {
        return {
            require: "ngModel",
            link: function (scope, el, attrs, ngModel) {
                //change event is fired when file is selected
                el.bind("change", function () {
                    scope.$apply(function () {
                        ngModel.$setViewValue(el.val());
                        ngModel.$render();
                    });
                });
            }
        }
    });

    // Controllers

    trackie_module.controller("MainController", ["$scope", "djangoAuth", "Restangular", function ($scope, djangoAuth, Restangular) {
        $scope.register = function (username, pass1, pass2, email) {
            djangoAuth.register(username, pass1, pass2, email).then(function (data) {
                djangoAuth.authenticationStatus(false, true).then(function () {
                    djangoAuth.changedAuth();
                });
            }, function (error) {
                renderFormErrors($("#registration-form"), error, "id_");
            });
        }
    }]);

    trackie_module.controller("ProfileController", ["$scope", "djangoAuth", "Restangular" ,function($scope, djangoAuth, Restangular){
        Restangular.all("auth").customGET("user/").then(function(user){
            $scope.user = user;
        });
    }]);

    trackie_module.controller("MapController", ["$scope", "$routeParams", "$interval", "Restangular", "uiGridConstants", function($scope, $routeParams, $interval, Restangular, uiGridConstants){
        function highlight_racers(scope, ol_source) {
        var selected = scope.gridApi.selection.getSelectedRows();
        var selectedIds = [];
        _.forEach(selected, function (i) {
            selectedIds.push(i.id);
        });
        ol_source.forEachFeature(function (i) {
            if (selected.length == 0 || _.indexOf(selectedIds, i.getId()) == -1) {
                i.setProperties({"$hide": false});
            } else {
                i.setProperties({"$hide": true});
            }
        });
    }

        function get_race_data(promise, scope, ol_source, projection) {
            promise.get().then(function (race_data) {
                if (race_data.status == 204) {
                    $interval.cancel(scope.data_interval);
                    console.log("Race stream has been ended");
                    return;
                }
                scope.race_data = race_data.data;
                scope.gridOptions.data = race_data.data.features;
                ol_source.clear();

                var format = new ol.format.GeoJSON();
                var features = format.readFeatures(race_data.data, {featureProjection: projection});
                ol_source.addFeatures(features);

                highlight_racers(scope, ol_source);
            }, function(response) {
                console.log(response);
            });
        }

        $scope.gridOptions = {
            primaryKey: "properties.racer.number",
            enableRowSelection: true,
            multiSelect: true,
            enableSelectAll: true,
            paginationPageSizes: false,
            paginationPageSize: 10,
            rowIdentity: function (row) {
                return row.properties.racer.number;
            },
            onRegisterApi: function(gridApi){
                $scope.gridApi = gridApi;
                $scope.gridApi.selection.on.rowSelectionChanged($scope, function(){
                    highlight_racers($scope, track_data_source);
                });
                $scope.gridApi.selection.on.rowSelectionChangedBatch($scope, function(){
                    highlight_racers($scope, track_data_source);
                });
            },
            columnDefs: [
                {name:"Číslo", field: "properties.racer.number"},
                {name:"Meno", field: "properties.racer.first_name"},
                {name:"Priezvisko", field: "properties.racer.last_name"},
                {name:"Čas", field: "properties.data.time"}
            ]
        };

        var race = Restangular.one("races", $routeParams.id);
        race.get().then(function(response){
            var projection = response.data.projection ? response.data.projection.code : "EPSG:3857";
            $scope.race = response.data;

            Restangular.oneUrl("tracks", $scope.race.track.file).get().then(function(json){
                var format = new ol.format.GPX();
                var features = format.readFeatures(json.data, {featureProjection: projection});
                var promise = race.one("data");

                track_source.addFeatures(features);
                map.getView().fit(map.getLayers().getArray()[1].getSource().getExtent(), map.getSize());

                get_race_data(promise, $scope, track_data_source, projection);
                if (!response.data.end) {
                    $scope.data_interval = $interval(function () {
                        get_race_data(promise, $scope, track_data_source, projection);
                    }, 5000);

                    $scope.$on("$destroy", function(){
                        $interval.cancel($scope.data_interval);
                    })
                }
            });
        });
    }]);

    trackie_module.controller("TrackCreateController", ["$scope", "$location", "Restangular", function($scope, $location, Restangular){
        $scope.trackForm = {};

        $scope.createTrack = function () {
            var data = angular.copy($scope.trackForm.data);
            data["file"] = data["file"] ? data["file"]["base64"] : null;
            Restangular.all("tracks").post(data).then(function(response){
                $location.path("/track/"+response.data.id);
            }, function(error){
                renderFormErrors($("#track-form"), error.data, "id_");
            });
        }
    }]);

    trackie_module.controller("TrackController", ["$scope", "$location", "$routeParams", "Restangular", "djangoAuth", function ($scope, $location, $routeParams, Restangular, djangoAuth) {
        djangoAuth.authenticationStatus().then(function(){
            $scope.user = djangoAuth.user;
        });

        $scope.track_source = Restangular.one("tracks", $routeParams.id);
        $scope.track_source.get().then(function (response) {
            $scope.track = response;
            Restangular.oneUrl("tracks", response.data.file).get().then(function (file) {
                var format = new ol.format.GPX();
                var features = format.readFeatures(file.data, {featureProjection: "EPSG:3857"});

                track_source.addFeatures(features);
                map.getView().fit(map.getLayers().getArray()[1].getSource().getExtent(), map.getSize());
            })
        }, function (error) {
            if (error.status.toString()[0] == 4){ //4xx
                $location.url("/" + error.status + "?from="+$location.path());
            }
        });
    }]);
}());
