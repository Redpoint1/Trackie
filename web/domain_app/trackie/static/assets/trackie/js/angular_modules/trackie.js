(function () {
    "use strict";
    var trackie_module = angular.module("trackie", ["ngRoute", "ngResource", "ngCookies", "restangular"])
        .config(["$interpolateProvider", function ($interpolateProvider) {
            $interpolateProvider.startSymbol("{$");
            $interpolateProvider.endSymbol("$}");
        }])
        .config(["$httpProvider", function ($httpProvider) {
            $httpProvider.defaults.xsrfCookieName = "csrftoken";
            $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken";
        }])
        .config(["RestangularProvider", function (RestangularProvider) {
            RestangularProvider.setBaseUrl("/api/v1");
            RestangularProvider.setRequestSuffix("/");
        }])
        .config(["$routeProvider", "$locationProvider", function ($routeProvider, $locationProvider) {
            $routeProvider.when("/", {
                templateUrl: "main.html",
                controller: "MainController"
            }).otherwise({
                redirectTo: "/"
            });

            //$locationProvider.html5Mode(true);
        }]);

    // Services

    trackie_module.service("djangoAuth", ["$q", "$http", "$cookies", "$rootScope", "$templateCache", function ($q, $http, $cookies, $rootScope, $templateCache) {
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
                    djangoAuth.authenticated = false;
                    djangoAuth.user = null;
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
                    this.authPromise = this.request({
                        "method": "GET",
                        "url": "/user/"
                    });
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
                            $templateCache.removeAll();
                        }
                        self.authenticated = true;
                        self.user = data;
                        defer.resolve();
                    }, function () {
                        if (self.authenticated) {
                            $templateCache.removeAll();
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
            "initialize": function (url, sessions) {
                this.API_URL = url || this.API_URL;
                this.use_session = sessions || this.use_session;
                return this.authenticationStatus();
            }
        };
    }]);

    // Directives

    trackie_module.directive("loginModal", ["djangoAuth", "$window", function (djangoAuth, $window) {
        function link(scope, element, attrs) {
            scope.djangoAuth = djangoAuth;
            scope.login = function (username, password) {
                djangoAuth.login(username, password).then(function (data) {
                    element.find("#login-modal").removeClass("in").hide();
                    element.find("#login-modal-backdrop").fadeOut().removeClass("in");
                    //location /home or if template have 2 modes route reload
                }, function (error) {
                    element.find("form").find(".error").remove();
                    for (var key in error){
                        var list = $("<ul class='error'></ul>");
                        for (var i=0; i < error[key].length; i++){
                            list.append("<li>" + error[key][i] + "</li>");
                        }
                        element.find("#"+key).append(list);
                    }
                });
            };
            scope.logout = function () {
                djangoAuth.logout().then(function () {
                    // nothing now, location / maybe?
                }, function () {
                    $window.alert("Nedá sa odhlásiť. Skúste to neskôr.")
                });
            }
        }

        return {
            link: link,
            restrict: "AE",
            templateUrl: "partials/login.html",
            scope: {}
        };
    }]);

    // Controllers

    trackie_module.controller("MainController", ["$scope", "djangoAuth", "Restangular", function ($scope, djangoAuth, Restangular) {
        djangoAuth.initialize();
    }]);
}());
