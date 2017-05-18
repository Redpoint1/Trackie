(function () {
    "use strict";
    var trackie_module = angular.module("trackie", ["ngRoute", "ngResource", "ngSanitize", "ngCookies", "ngAnimate", "ngTouch", "restangular", "ui.grid", "ui.grid.selection", "ui.grid.saveState", "ui.grid.pagination", "ui.grid.autoResize", "naif.base64"])
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
                        var keysToDelete = _.filter($delegate.getKeys(), function (n) {
                            return regex.test(n);
                        });
                        _.forEach(keysToDelete, function (key) {
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
        .config(["$resourceProvider", function ($resourceProvider) {
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
            }).when("/race-fields/add", {
                templateUrl: "partials/race_type/create.html",
                controller: "TypeCreateController",
                reloadAfterAuthChange: true,
                throwAuthError: true,
                noCacheTemplate: true
            }).when("/race-fields/:id", {
                templateUrl: "partials/race_type/detail.html",
                controller: "TypeController",
                reloadAfterAuthChange: true
            }).when("/race-fields/:id/update", {
                templateUrl: "partials/race_type/update.html",
                controller: "TypeUpdateController",
                reloadAfterAuthChange: true,
                throwAuthError: true,
                noCacheTemplate: true
            }).when("/races/add", {
                templateUrl: "partials/race/create.html",
                controller: "RaceCreateController",
                reloadAfterAuthChange: true,
                throwAuthError: true,
                noCacheTemplate: true
            }).when("/race/:id", {
                templateUrl: "partials/race/detail.html",
                controller: "RaceController"
            }).when("/race/:id/update", {
                templateUrl: "partials/race/update.html",
                controller: "RaceUpdateController",
                reloadAfterAuthChange: true,
                throwAuthError: true,
                noCacheTemplate: true
            }).when("/race/:id/participants", {
                templateUrl: "partials/racer_in_race/create.html",
                controller: "RacerInRaceCreateController",
                reloadAfterAuthChange: true,
                throwAuthError: true,
                noCacheTemplate: true
            }).when("/track/add", {
                templateUrl: "partials/track/create.html",
                controller: "TrackCreateController",
                reloadAfterAuthChange: true,
                throwAuthError: true
            }).when("/track/:id", {
                templateUrl: "partials/track/detail.html",
                controller: "TrackController",
                reloadAfterAuthChange: true
            }).when("/track/:id/update", {
                templateUrl: "partials/track/update.html",
                controller: "TrackUpdateController",
                reloadAfterAuthChange: true,
                throwAuthError: true
            }).when("/racer/add", {
                templateUrl: "partials/racer/create.html",
                controller: "RacerCreateController",
                reloadAfterAuthChange: true,
                throwAuthError: true
            }).when("/racer/:id", {
                templateUrl: "partials/racer/detail.html",
                controller: "RacerController"
            }).when("/racer/:id/update", {
                templateUrl: "partials/racer/update.html",
                controller: "RacerUpdateController"
            }).when("/sports/:id", {
                templateUrl: "partials/sport_type/detail.html",
                controller: "SportDetailController"
            }).when("/search", {
                templateUrl: "partials/search/all.html",
                controller: "SearchAllController"
            }).when("/tournaments", {
                templateUrl: "partials/tournament/list.html",
                controller: "TournamentsController"
            }).when("/tournaments/add", {
                templateUrl: "partials/tournament/create.html",
                controller: "TournamentCreateController",
                reloadAfterAuthChange: true,
                throwAuthError: true,
                noCacheTemplate: true
            }).when("/tournament/:id", {
                templateUrl: "partials/tournament/detail.html",
                controller: "TournamentController",
                reloadAfterAuthChange: true
            }).when("/tournament/:id/update", {
                templateUrl: "partials/tournament/update.html",
                controller: "TournamentUpdateController",
                reloadAfterAuthChange: true,
                throwAuthError: true,
                noCacheTemplate: true
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
        .run(["$rootScope", "$location", "$route", "$templateCache", "djangoAuth", function ($rootScope, $location, $route, $templateCache, djangoAuth) {
            djangoAuth.initialize();
            $rootScope.$on("$routeChangeStart", function (event, toState, toParams) {
                var state = toState.redirectTo ? $route.routes[toState.redirectTo] : toState;
                djangoAuth.authenticationStatus().then(function () {
                    djangoAuth.checkPageAuth(state.throwAuthError);
                });

                var template = $templateCache.get(state.$$route.templateUrl);
                if (state.$$route.noCacheTemplate && template){
                    $templateCache.remove(state.$$route.templateUrl);
                    $route.reload();
                }
            });
        }]);

    // Filters

    trackie_module.filter('capitalize', function () {
        return function (input) {
            return (!!input) ? input.charAt(0).toUpperCase() + input.substr(1).toLowerCase() : '';
        }
    });

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
                    var from = $route.current.params.from || "/";
                    // not good for dynamic routes like /tracks/:id
                    var route = $route.routes[from] || {};
                    if (route.throwAuthError) {
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

    // Factories

    trackie_module.factory("OLMap", [function () {
        function OLMapFactory(target, scope) {
            this.target = target;
            this.fit = null;
            this.sources = {};
            this.sidebar = null;
            this.layers = {
                "tile": new ol.layer.Tile({
                    source: new ol.source.OSM()
                })
            };
            this.interactions = {};
            this.selectedFeature = null;
            this.focusOnRacer = null;
            this.style = {
                "Point": new ol.style.Style({
                    image: new ol.style.Icon({
                        anchor: [0.5, 1],
                        src: "/static/assets/trackie/img/marker.png",
                        opacity: 1,
                        scale: 0.4
                    })
                }),
                "Point_selected": new ol.style.Style({
                    image: new ol.style.Icon({
                        anchor: [0.5, 1],
                        src: "/static/assets/trackie/img/marker_select.png",
                        opacity: 1,
                        scale: 0.4
                    })
                }),
                "Point_unselected": new ol.style.Style({
                    image: new ol.style.Icon({
                        anchor: [0.5, 1],
                        src: "/static/assets/trackie/img/marker.png",
                        opacity: 0.3,
                        scale: 0.4
                    })
                }),
                "LineString": new ol.style.Style({
                    stroke: new ol.style.Stroke({
                        color: "green",
                        width: 1
                    })
                }),
                "MultiLineString": new ol.style.Style({
                    stroke: new ol.style.Stroke({
                        color: "green",
                        width: 1
                    })
                })
            };
            this.map = new ol.Map({
                layers: [
                    this.layers.tile
                ],
                view: new ol.View({
                    center: [0, 0],
                    zoom: 1
                })
            });
            var self=this;
            scope.$watch("$viewContentLoaded", function () {
                var interval = setInterval(function () {
                    var element = $(".map").filter("#" + self.target);
                    if (element.length == 1) {
                        self.map.setTarget(element[0]);
                        if (self.fit) self.fitBySource(self.fit);
                        clearInterval(interval);
                    }
                }, 500);
            });
        }

        OLMapFactory.prototype.addVectorLayer = function (options) {
            var name = options.name;
            var source = !options["source"] ? new ol.source.Vector() : options.source;
            var style = options["style"] ? options["style"] : undefined;

            var layer = new ol.layer.Vector({
                source: source,
                style: style
            });

            this.sources[name] = source;
            this.layers[name] = layer;
            this.map.addLayer(layer);

            return layer;
        };

        OLMapFactory.prototype.addSidebar = function (options) {
            var self = this;
            var interval = setInterval(function(){
                if (self.map.getTarget()){
                    self.sidebar = new ol.control.Sidebar(options);
                    self.map.addControl(self.sidebar);
                    clearInterval(interval);
                }
            }, 100);
        };

        OLMapFactory.prototype.openSidebar = function (tab_name) {
            if (!this.sidebar) {
                return;
            }
            this.sidebar.open(tab_name);
        };

        OLMapFactory.prototype.closeSidebar = function () {
            if (!this.sidebar) {
                return;
            }
            this.sidebar.close();
        };

        OLMapFactory.prototype.fitBySource = function (name) {
            this.fit = name;
            this.map.getView().fit(this.sources[name].getExtent());
        };

        OLMapFactory.prototype.clearSource = function (name) {
            this.sources[name].clear();
        };

        OLMapFactory.prototype.addFeaturesForSource = function (options) {
            this.sources[options.name].addFeatures(options.features);
        };

        OLMapFactory.prototype.selectFeature = function (feature) {
            this.selectedFeature = feature;
        };

        OLMapFactory.prototype.readFeaturesFromGPX = function (data) {
            var format = new ol.format.GPX();
            var features = format.readFeatures(data, {featureProjection: "EPSG:3857"});

            return features;
        };

        OLMapFactory.prototype.readFeaturesFromGeoJSON = function (options) {
            var format = new ol.format.GeoJSON();
            var features = format.readFeatures(options.data, {featureProjection: options.projection});

            return features;
        };

        OLMapFactory.prototype.destroy = function () {
            this.map.setTarget(null);
            return null;
        };

        OLMapFactory.prototype.toggleRacerFocus = function (racer, source) {
            if (racer.id == this.focusOnRacer) {
                this.focusOnRacer = null;
            } else {
                this.focusOnRacer = racer.id;
                this.setCenter(source);
            }
        };

        OLMapFactory.prototype.setCenter = function (source) {
            var self = this;
            this.sources[source].forEachFeature(function (feature) {
                if (feature.getProperties().racer.id == self.focusOnRacer) {
                    self.map.getView().setCenter(feature.getGeometry().getExtent());
                }
            });
        };

        OLMapFactory.prototype.destroy = function(){
            this.map.setTarget(null);
            this.map = null;
        };

        return OLMapFactory;
    }]);

    trackie_module.factory("Player", ["Restangular", function (Restangular) {
        function Player(element, scope) {
            this.scope = scope;
            this.element = element;
            this.timezone = moment.tz.guess();
            this.start = moment(scope.race.real_start);
            this.end = moment(scope.race.real_end);
            this.total_count = scope.race.records_count;
            this.scope.play = false;
            this.scope.diff_time = true;
            this.step = 0;
            this.data = [];

            var top_position = 0;
            var timestamp = $(
                "<div class='timestamp'>" +
                "<div class='timestamp-body'>" +
                "<div class='timestamp-text'></div>" +
                "<div class='timestamp-bottom'>" +
                "<div class='timestamp-caret'></div>" +
                "</div></div></div>"
            );
            $("body").append(timestamp);
            var self = this;
            element.find(".player-progress-bar")
                .on("mousemove", function (e) {
                    e.preventDefault();
                    var step = Math.floor((e.offsetX) / (($(e.currentTarget).width()) / self.total_count));
                    if (step > self.loaded_records()) {
                        timestamp.hide();
                    } else {
                        timestamp.show();
                        timestamp.offset({
                            top: top_position - timestamp.height() - 15,
                            left: e.clientX - timestamp.width() / 2
                        });
                        timestamp.find(".timestamp-text").text(self.timestamp(step));
                    }
                })
                .on("mouseleave", function () {
                    timestamp.hide();
                })
                .on("mouseenter", function (e) {
                    var bar = $(e.currentTarget);
                    top_position = bar.offset().top;
                })
                .on("click", function (e) {
                    e.preventDefault();
                    var step = Math.floor((e.offsetX) / (($(e.currentTarget).width()) / self.total_count));
                    if (step > self.loaded_records()) {
                        timestamp.hide();
                    } else {
                        self.setStep(step + 1);
                    }
                });
        }

        Player.prototype.setData = function (data, i) {
            var parsed_data = [];
            var self = this;
            _.forEach(data, function (record) {
                parsed_data.push(self.parseRecord(record));
            });
            Array.prototype.push.apply(this.data, parsed_data);
        };

        Player.prototype.parseRecord = function (record) {
            return {
                time: this.getDateFromRecord(record),
                data: record
            }
        };

        Player.prototype.getDateFromRecord = function (record) {
            return moment(record.features[0].properties.received);
        };

        Player.prototype.loadData = function (race, from) {
            var from_timestamp = from ? from.utc().valueOf() : "";
            if (!this.complete()) {
                var self = this;
                Restangular.one("races", race).getList("replay", {from: from_timestamp}).then(function (response) {
                    self.setData(response.data.plain());
                    self.element.find(".player-progress-bar-done").width("calc(100% / " + self.total_count + " * " + self.loaded_records() + ")");
                    self.loadData(race, self.getLastRecordTimestamp());
                });
            }
        };

        Player.prototype.complete = function () {
            return this.end.isSame(this.getLastRecordTimestamp());
        };

        Player.prototype.getLastRecordTimestamp = function () {
            var record = this.data[this.data.length - 1];
            if (record) {
                return record.time;
            }
            return moment(0);
        };

        Player.prototype.resume = function (skip_inc) {
            if (this.step >= (this.loaded_records())) return;
            this.scope.play = true;
            this.scope.$applyAsync();
            this.render(skip_inc);
            var self = this;
            this.interval = setInterval(function () {
                self.render();
            }, 1000 / this.scope.play_speed);
        };

        Player.prototype.stop = function () {
            this.scope.play = false;
            this.scope.$applyAsync();
            clearInterval(this.interval);
        };

        Player.prototype.togglePlay = function () {
            if (this.scope.play)
                this.stop();
            else
                this.resume();
        };

        Player.prototype.render = function (skip_inc) {
            if (this.scope.play && !skip_inc) this.step++;
            var step = Math.max(this.step - 1, 0);
            this.element.find(".player-progress-bar-played").width("calc(100% / " + this.total_count + " * " + this.step + ")");
            this.element.find(".player-progress-bar-text").text(this.timestamp(step));
            if (this.data.length)
                this.scope.$parent.set_data(this.data[step].data);
            if (this.step >= this.loaded_records()) {
                this.stop();
            }
        };

        Player.prototype.loaded_records = function () {
            return this.data.length;
        };

        Player.prototype.timestamp = function (step) {
            var result = this.data[step];
            result = result ? result.time : this.start;

            if (this.scope.diff_time) {
                return moment(result.diff(this.start)).utc().format("HH:mm:ss");
            }
            return result.tz(window.timezone).format("HH:mm:ss");
        };

        Player.prototype.setStep = function (step) {
            this.step = step;
            if (this.scope.play) {
                this.stop();
                this.resume(true);
            } else {
                this.render(true);
            }
        };

        Player.prototype.destroy = function () {
            clearInterval(this.interval);
        };

        return Player;
    }]);

    trackie_module.factory("GridOptionsGenerator", [function () {
        function GridOptionsGenerator() {
            // ui-grid field types
            // 'string'
            // 'boolean'
            // 'number'
            // 'date'
            // 'object'
            // 'numberStr
            this.fields = {
                "BigIntegerField": "number",
                "BooleanField": "boolean",
                "DateField": "date",
                "DateTimeField": "date",
                "DurationField": "date",
                "FloatField": "number",
                "IntegerField": "number",
                "PositiveIntegerField": "number",
                "PositiveSmallIntegerField": "number",
                "SmallIntegerField": "number",
                "TextField": "string",
                "TimeField": "date",
                "URLField": "string"
            }
        }

        GridOptionsGenerator.prototype.generate = function (scope) {
            var options = {
                primaryKey: "properties.racer.number",
                enableRowSelection: true,
                multiSelect: true,
                enableSelectAll: true,
                paginationPageSizes: false,
                paginationPageSize: 10,
                rowIdentity: function (row) {
                    return row.properties.racer.number;
                },
                onRegisterApi: function (gridApi) {
                    scope.gridApi = gridApi;
                    scope.gridApi.selection.on.rowSelectionChanged(scope, function () {
                        scope.highlight_racers("data");
                    });
                    scope.gridApi.selection.on.rowSelectionChangedBatch(scope, function () {
                        $timeout(function () {
                            scope.highlight_racers("data");
                        });
                    });
                },
                columnDefs: [
                    {name: "Číslo", field: "properties.racer.number"},
                    {name: "Meno", field: "properties.racer.first_name"},
                    {name: "Priezvisko", field: "properties.racer.last_name"}
                ]
            };

            for (var i = 0; i < scope.race.type.fields.length; i++) {
                var new_field = scope.race.type.fields[i];
                options.columnDefs.push({
                    name: new_field.display_name,
                    field: "properties.data." + new_field.name,
                    type: this.fields[new_field.type]
                })
            }

            return options;
        };

        return GridOptionsGenerator;
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

    trackie_module.directive("player", ["Player", function (Player) {
        function link(scope, element) {
            scope.play_speed = "1";

            scope.$parent.$watch("race", function (newItem) {
                if (newItem && newItem.end && !scope.player) {
                    scope.player = new Player(element, scope);
                    scope.$parent.player = scope.player;
                }
            });

            scope.$watch("play_speed", function (newValue) {
                if (newValue && scope.player && scope.play) {
                    scope.player.stop();
                    scope.player.resume();
                }
            });

            scope.$watch("diff_time", function () {
                if (scope.player) scope.player.render(true);
            });
        }

        return {
            link: link,
            restrict: "E",
            templateUrl: "partials/player.html",
            scope: true
        };
    }]);

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

    trackie_module.controller("ProfileController", ["$scope", "djangoAuth", "Restangular", function ($scope, djangoAuth, Restangular) {
        Restangular.all("auth").customGET("user/").then(function (user) {
            $scope.user = user;
        });
    }]);

    trackie_module.controller("RaceCreateController", ["$scope", "$location", "Restangular", function ($scope, $location, Restangular) {
        $scope.createRace = function () {
            Restangular.all("races").post($scope.raceForm.data).then(function (response) {
                $location.path("/race/" + response.data.id + "/participants");
            }, function (error) {
                renderFormErrors($("#race-form"), error.data, "id_");
            });
        };
    }]);

    trackie_module.controller("RacerInRaceCreateController", ["$scope", "$location", "$routeParams", "Restangular", function ($scope, $location, $routeParams, Restangular) {
        $scope.increase = function () {
            $scope.racerInRaceForm.data.push({});
            $scope.$applyAsync();
        };

        $scope.reduce = function(){
            if ($scope.racerInRaceForm.data.length > $scope.participants.length) $scope.racerInRaceForm.data.pop();
            $scope.$applyAsync();
        };

        $scope.range = function(n) {
            n = n || 0;
            return new Array(n);
        };

        $scope.addParticipants = function () {
            var data = [];
            $.each($scope.racerInRaceForm.data, function(i,n) {
                if(!n.remove){
                    delete n["remove"];
                    delete n["race"];
                    delete n["id"];
                    data.push(n);
                }
            });
            Restangular.one("races", $routeParams.id).all("participants").post(data).then(function (response) {
                $location.path("/race/" + $routeParams.id);
            }, function (error) {
                renderFormErrors($("#participant-form"), error.data, "id_");
            });
        };

        Restangular.one("races", $routeParams.id).all("participants").getList().then(function (response) {
            _.each(response.data, function(temp, i){
                response.data[i].racer = String(response.data[i].racer.id);
            });

            $scope.participants = response.data;
            $scope.racerInRaceForm.data = response.data.plain();

            if (!$scope.racerInRaceForm.data.length){
                $scope.increase();
            }
        }, function (error) {
            if (error.status.toString()[0] == 4) { //4xx
                $location.url("/" + error.status + "?from=" + $location.path());
            }
        });
    }]);

    trackie_module.controller("RaceUpdateController", ["$scope", "$location", "$routeParams", "Restangular", function ($scope, $location, $routeParams, Restangular) {
        $scope.updateRace = function () {
            $scope.race = angular.extend($scope.race, $scope.raceForm.data);
            $scope.race.put().then(function (response) {
                $location.path("/race/" + response.data.id);
            }, function (error) {
                renderFormErrors($("#race-form"), error.data, "id_");
            });
        };

        function getItFrom(model){
            if (model){
                return "" + model.id;
            }
            return null;
        }

        Restangular.one("races", $routeParams.id).get().then(function (response) {
            $scope.race = response.data;
            $scope.race.tournament = getItFrom($scope.race.tournament);
            $scope.race.type = getItFrom($scope.race.type);
            $scope.race.track = getItFrom($scope.race.track);
            $scope.race.projection = getItFrom($scope.race.projection);
            $scope.raceForm.data = response.data.plain();
            console.log($scope.race);
        }, function (error) {
            if (error.status.toString()[0] == 4) { //4xx
                $location.url("/" + error.status + "?from=" + $location.path());
            }
        })
    }]);

    trackie_module.controller("RaceController", ["$scope", "$location", "$routeParams", "$timeout", "$interval", "Restangular", "OLMap", "GridOptionsGenerator", function ($scope, $location, $routeParams, $timeout, $interval, Restangular, OLMap, GridOptionsGenerator) {
        $scope.highlight_racers = function (source) {
            if (!$scope.gridApi) return source;
            var selected_features = $scope.gridApi.selection.getSelectedRows();
            var all_selected = $scope.gridApi.selection.getSelectAllState();
            var selectedIds = [];
            var selectedInMapId = $scope.map.selectedFeature ? $scope.map.selectedFeature.getProperties().racer.id : null;

            _.forEach(selected_features, function (selected_fature) {
                selectedIds.push(selected_fature.properties.racer.id);
            });

            if (typeof source == "string") {
                $scope.map.sources[source].forEachFeature(function (feature) {
                    var featureId = feature.getProperties().racer.id;
                    if (selected_features.length == 0 || all_selected || _.indexOf(selectedIds, featureId) > -1) {
                        feature.setProperties({"$hide": false});
                    } else {
                        feature.setProperties({"$hide": true});
                    }

                    if (selectedInMapId && selectedInMapId == featureId) {
                        feature.setProperties({"$selected": true});
                    } else {
                        feature.setProperties({"$selected": false});
                    }
                });
            } else {
                _.forEach(source, function (feature) {
                    var featureId = feature.getProperties().racer.id;
                    if (selected_features.length == 0 || all_selected || _.indexOf(selectedIds, featureId) > -1) {
                        feature.setProperties({"$hide": false});
                    } else {
                        feature.setProperties({"$hide": true});
                    }

                    if (selectedInMapId && selectedInMapId == featureId) {
                        feature.setProperties({"$selected": true});
                    } else {
                        feature.setProperties({"$selected": false});
                    }
                });
            }
            return source;
        };

        $scope.set_data = function (data) {
            $scope.race_data = data;
            $scope.gridOptions.data = data.features;
            $scope.map.clearSource("data");

            var features = $scope.map.readFeaturesFromGeoJSON({
                data: data,
                projection: $scope.projection
            });
            features = $scope.highlight_racers(features);

            $scope.map.addFeaturesForSource({
                name: "data",
                features: features
            });
            $scope.map.setCenter("data");
            $scope.$applyAsync();
        };

        $scope.get_race_data = function (promise) {
            promise.get().then(function (race_data) {
                if (race_data.status == 204) {
                    $interval.cancel($scope.data_interval);
                    $scope.endOfRace = true;
                    if ($scope.race.end) return;
                    $scope.race_rest.get().then(function (response) {
                        $scope.race = response.data;
                    }, function (error) {
                    });
                    return;
                }
                $scope.set_data(race_data.data);
            }, function (response) {
                console.log(response);
            });
        };

        $scope.replay = function () {
            $scope.endOfRace = false;
            $scope.showPlayer = true;
            $scope.player.loadData($routeParams.id);
        };

        $scope.endOfRace = false;
        $scope.showPlayer = false;
        $scope.player = null;

        $scope.map = new OLMap("map", $scope);
        $scope.map.addVectorLayer({name: "track"});
        $scope.map.addVectorLayer({
            name: "data",
            style: function (feature) {
                var type = feature.getGeometry().getType();
                if (feature.getProperties()["$hide"]) {
                    type += "_unselected";
                } else if (feature.getProperties()["$selected"]) {
                    type += "_selected";
                }
                return $scope.map.style[type];
            }
        });

        $scope.map.map.on("click", function (event) {
            $scope.map.map.forEachFeatureAtPixel(event.pixel, function (feature) {
                if (feature.getGeometry().getType() == "Point") {
                    if ($scope.map.selectedFeature && $scope.map.selectedFeature.getProperties().racer.id == feature.getProperties().racer.id) {
                        $scope.map.selectedFeature = null;
                    } else {
                        $scope.map.selectedFeature = feature;
                    }
                    $scope.highlight_racers("data");

                    if (!$scope.map.selectedFeature) {
                        $scope.map.closeSidebar();
                        return;
                    }
                    var _racer = feature.getProperties()["racer"];
                    var regex = new RegExp(Restangular.configuration.baseUrl + "(.*)$");
                    var endpoint = regex.exec(_racer.url);
                    Restangular.oneUrl(endpoint[1]).get().then(function (response) {
                        if (response.status == 200) {
                            $scope.racer = response.data;
                            $scope.map.openSidebar("profile");
                        }
                    })
                }
            }, {
                hitTolerance: 5
            });
        });

        $(".sidebar-close").on("click", function () {
            $scope.map.selectedFeature = null;
            $scope.highlight_racers("data");
        });

        $scope.map.addSidebar({element: "sidebar", position: "left"});

        $scope.race_rest = Restangular.one("races", $routeParams.id);
        $scope.race_rest.get().then(function (response) {
            $scope.projection = response.data.projection ? response.data.projection.code : "EPSG:3857";
            $scope.race = response.data;

            $scope.gridOptions = new GridOptionsGenerator().generate($scope);

            Restangular.oneUrl("tracks", $scope.race.track.file).get().then(function (json) {
                var promise = $scope.race_rest.one("data");

                $scope.map.addFeaturesForSource({
                    name: "track",
                    features: $scope.map.readFeaturesFromGPX(json.data)
                });
                $scope.map.fitBySource("track");

                if ($scope.race.end) {
                    $scope.endOfRace = true;
                    return;
                }
                $scope.get_race_data(promise);
                if (!response.data.end) {
                    $scope.data_interval = $interval(function () {
                        $scope.get_race_data(promise);
                    }, 1000);

                    $scope.$on("$destroy", function () {
                        $interval.cancel($scope.data_interval);
                    })
                }
            });
        }, function (error) {
            if (error.status.toString()[0] == 4) { //4xx
                $location.url("/" + error.status + "?from=" + $location.path());
            }
        });

        $scope.$on("$destroy", function(e){
            if (e.targetScope == e.currentScope){
                $scope.map.destroy();
                $scope.player.destroy();
            }
        });
    }]);

    trackie_module.controller("TrackCreateController", ["$scope", "$location", "Restangular", "OLMap", function ($scope, $location, Restangular, OLMap) {
        $scope.trackForm = {};

        $scope.createTrack = function () {
            var data = angular.copy($scope.trackForm.data);
            data["file"] = data["file"] ? data["file"]["base64"] : null;
            Restangular.all("tracks").post(data).then(function (response) {
                $location.path("/track/" + response.data.id);
            }, function (error) {
                renderFormErrors($("#track-form"), error.data, "id_");
            });
        };

        $scope.trackPreview = function () {
            if (!$scope.trackForm.data["file"]) {
                $scope.map = $scope.map.destroy();
            } else {
                $scope.map = new OLMap("track-preview", $scope);
                $scope.map.addVectorLayer({name: "track"});
                $scope.map.clearSource("track");
                $scope.map.addFeaturesForSource({
                    name: "track",
                    features: $scope.map.readFeaturesFromGPX(
                        atob($scope.trackForm.data["file"]["base64"])
                    )
                });
                $scope.map.fitBySource("track");
            }
        };
    }]);

    trackie_module.controller("TrackController", ["$scope", "$location", "$routeParams", "Restangular", "djangoAuth", "OLMap", function ($scope, $location, $routeParams, Restangular, djangoAuth, OLMap) {
        $scope.deleteTrack = function () {
            $scope.track.remove().then(function (response) {
                $location.path("/");
            }, function (error) {
                if (error.status.toString()[0] == 4) { //4xx
                    $location.url("/" + error.status + "?from=" + $location.path());
                }
            })
        };

        $scope.map = new OLMap("track-map", $scope);
        $scope.map.addVectorLayer({name: "track"});

        djangoAuth.authenticationStatus().then(function () {
            $scope.user = djangoAuth.user;
        });

        $scope.track_source = Restangular.one("tracks", $routeParams.id);
        $scope.track_source.get().then(function (response) {
            $scope.track = response.data;
            Restangular.oneUrl("tracks", response.data.file).get().then(function (file) {
                $scope.map.addFeaturesForSource({
                    name: "track",
                    features: $scope.map.readFeaturesFromGPX(file.data)
                });
                $scope.map.fitBySource("track");
            })
        }, function (error) {
            if (error.status.toString()[0] == 4) { //4xx
                $location.url("/" + error.status + "?from=" + $location.path());
            }
        });
    }]);

    trackie_module.controller("TrackUpdateController", ["$scope", "$location", "$routeParams", "Restangular", function ($scope, $location, $routeParams, Restangular) {
        $scope.updateTrack = function () {
            $scope.track = angular.extend($scope.track, $scope.trackForm.data);
            $scope.track.put().then(function (response) {
                $location.path("/track/" + response.data.id);
            }, function (error) {
                if (error.status.toString()[0] == 4) { //4xx
                    $location.url("/" + error.status + "?from=" + $location.path());
                }
            })
        };

        Restangular.one("tracks", $routeParams.id).get().then(function (response) {
            $scope.track = response.data;
            $scope.trackForm.data = response.data.plain();
        }, function (error) {
            if (error.status.toString()[0] == 4) { //4xx
                $location.url("/" + error.status + "?from=" + $location.path());
            }
        });
    }]);

    trackie_module.controller("RacerCreateController", ["$scope", "$location", "Restangular", function ($scope, $location, Restangular) {
        $scope.racerForm = {};

        $scope.createRacer = function () {
            var data = angular.copy($scope.racerForm.data);
            data["photo"] = data["photo"] ? data["photo"]["base64"] : null;
            Restangular.all("racers").post(data).then(function (response) {
                $location.path("/racer/" + response.data.id);
            }, function (error) {
                renderFormErrors($("#racer-form"), error.data, "id_");
            });
        }
    }]);

    trackie_module.controller("RacerController", ["$scope", "$location", "$routeParams", "Restangular", "djangoAuth", function ($scope, $location, $routeParams, Restangular, djangoAuth) {
        djangoAuth.authenticationStatus().then(function () {
            $scope.auth = djangoAuth;
        });

        $scope.time = function(timestamp){
            var time = moment(timestamp).tz(window.timezone);
            return time.format("L LTS");
        };

        $scope.duration_time = function (row) {
            var start = moment(row.entity.real_start);
            var end = moment(row.entity.real_end);
            return moment(end.diff(start)).utc().format("HH:mm:ss");
        };

        $scope.render_link = function (grid, row, col) {
            var url = "#/";
            switch (col.field) {
                case "tournament.sport.name":
                    url = "#/sport/" + row.entity.tournament.sport.slug;
                    break;
                case "tournament.name":
                    url = "#/tournament/" + row.entity.tournament.id;
                    break;
                case "type.name":
                    url = "#/race-type/" + row.entity.type.slug;
                    break;
                case "name":
                    url = "#/race/" + row.entity.id;
                    break;
            }

            return '<a href="' + url + '">' + grid.getCellValue(row, col) + '</a>'
        };

        $scope.gridPast = {
            paginationPageSizes: [10, 20, 50],
            onRegisterApi: function (gridApi) {
                $scope.gridPastApi = gridApi;
            },
            columnDefs: [
                {name: "Šport", field: "tournament.sport.name", cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.render_link(grid, row, col)"><div>'},
                {name: "Typ", field: "type.name", cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.render_link(grid, row, col)"><div>'},
                {name: "Turnaj", field: "tournament.name", cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.render_link(grid, row, col)"><div>'},
                {name: "Preteky", field: "name", cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.render_link(grid, row, col)"><div>'},
                {name: "Štart", field: "start", cellTemplate:'<div class="ui-grid-cell-contents">{{grid.appScope.time(grid.getCellValue(row, col))}}</div>'},
                {name: "Trvanie", field: "", cellTemplate:'<div class="ui-grid-cell-contents">{{grid.appScope.duration_time(row)}}</div>'}
            ]
        };

        $scope.gridCurrent = {
            paginationPageSizes: [10, 20, 50],
            onRegisterApi: function (gridApi) {
                $scope.gridPastApi = gridApi;
            },
            columnDefs: [
                {name: "Šport", field: "tournament.sport.name", cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.render_link(grid, row, col)"><div>'},
                {name: "Typ", field: "type.name", cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.render_link(grid, row, col)"><div>'},
                {name: "Turnaj", field: "tournament.name", cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.render_link(grid, row, col)"><div>'},
                {name: "Preteky", field: "name", cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.render_link(grid, row, col)"><div>'},
                {name: "Štart", field: "start", cellTemplate:'<div class="ui-grid-cell-contents">{{grid.appScope.time(grid.getCellValue(row, col))}}</div>'},
                {name: "Trvanie", field: "estimated_duration", cellTemplate:'<div class="ui-grid-cell-contents">~{{grid.getCellValue(row, col)}} min.</div>'}
            ]
        };

        $scope.gridFuture = {
            paginationPageSizes: [10, 20, 50],
            onRegisterApi: function (gridApi) {
                $scope.gridFutureApi = gridApi;
            },
            columnDefs: [
                {name: "Šport", field: "tournament.sport.name", cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.render_link(grid, row, col)"><div>'},
                {name: "Typ", field: "type.name", cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.render_link(grid, row, col)"><div>'},
                {name: "Turnaj", field: "tournament.name", cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.render_link(grid, row, col)"><div>'},
                {name: "Preteky", field: "name", cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.render_link(grid, row, col)"><div>'},
                {name: "Štart", field: "start", cellTemplate:'<div class="ui-grid-cell-contents">{{grid.appScope.time(grid.getCellValue(row, col))}}</div>'},
                {name: "Trvanie", field: "estimated_duration", cellTemplate:'<div class="ui-grid-cell-contents">~{{grid.getCellValue(row, col)}} min.</div>'}
            ]
        };

        $scope.racer_source = Restangular.one("racers", $routeParams.id);
        $scope.racer_source.get().then(function (response) {
            $scope.racer = response.data;

            $scope.race_finished = Restangular.all("races").one("racer", $scope.racer.id).all("finished").getList().then(function (response) {
                $scope.gridPast.data = response.data.plain();
            });

             $scope.race_finished = Restangular.all("races").one("racer", $scope.racer.id).all("active").getList().then(function (response) {
                $scope.gridCurrent.data = response.data.plain();
            });

            $scope.race_upcoming = Restangular.all("races").one("racer", $scope.racer.id).all("upcoming").getList().then(function (response) {
                $scope.gridFuture.data = response.data.plain();
            });
        });
    }]);

    trackie_module.controller("RacerUpdateController", ["$scope", "$location", "$routeParams", "Restangular", function ($scope, $location, $routeParams, Restangular) {
        $scope.updateRacer = function () {
            $scope.racer = angular.extend($scope.racer, $scope.racerForm.data);
            if (!$scope.racerForm.data["photo"]["base64"]) {
                delete $scope.racer["photo"];
                $scope.racer.patch().then(function (response) {
                    $location.path("/racer/" + response.data.id);
                }, function (error) {
                    renderFormErrors($("#racer-form"), error.data, "id_");
                });
            } else {
                $scope.racer.photo = $scope.racer.photo["base64"];
                $scope.racer.put().then(function (response) {
                    $location.path("/racer/" + response.data.id);
                }, function (error) {
                    renderFormErrors($("#racer-form"), error.data, "id_");
                });
            }
        };

        Restangular.one("racers", $routeParams.id).get().then(function (response) {
            $scope.racer = response.data;
            $scope.racerForm.data = response.data.plain();
        }, function (error) {
            if (error.status.toString()[0] == 4) { //4xx
                $location.url("/" + error.status + "?from=" + $location.path());
            }
        });
    }]);

    trackie_module.controller("SportDetailController", ["$scope", "$location", "$routeParams", "Restangular", function ($scope, $location, $routeParams, Restangular) {
        $scope.render_link = function (grid, row, col) {
            var url = "#/tournament/" + row.entity.id;
            return '<a href="' + url + '">' + grid.getCellValue(row, col) + '</a>';
        };

        $scope.grid = {
            paginationPageSizes: [10, 20, 50],
            onRegisterApi: function (gridApi) {
                $scope.gridApi = gridApi;
            },
            columnDefs: [
                {name: "Turnaj", field: "name", cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.render_link(grid, row, col)"><div>'},
            ]
        };
        $scope.sport_source = Restangular.one("sport-types", $routeParams.id);
        $scope.sport_source.get().then(function (response) {
            $scope.sport = response.data;

            $scope.tournaments = Restangular.one("sport-types", $routeParams.id).all("tournaments").getList().then(function (response) {
                $scope.grid.data = response.data.plain();
            });
        }, function(error){
            if (error.status.toString()[0] == 4) { //4xx
                $location.url("/" + error.status + "?from=" + $location.path());
            }
        });
    }]);
    
    trackie_module.controller("SearchBarController", ["$scope", "$location", function ($scope, $location) {
        $scope.minlength = 3;

        $scope.searchIt = function () {
            $location.url("/search?q=" + $scope.search_text);
        }
    }]);

    trackie_module.controller("SearchAllController", ["$scope", "$location", "$routeParams", "$timeout", "Restangular", function ($scope, $location, $routeParams, $timeout, Restangular) {
        $scope.q = $routeParams.q;
        $scope.result = null;
        $scope.resultCategory = [];

        $scope.categoryTranslate = function(key){
            var sk = {
                "tournament": "Turnaj",
                "track": "Trať",
                "racer": "Pretekár",
                "race": "Závod"
            };

            return sk.hasOwnProperty(key) ? sk[key] : key;
        };

        $scope.showSearchResult = function(key) {
            $(".search-category").find("li").removeClass("active");
            $("#" + key).addClass("active");
            $scope.resultCategory = $scope.result[key];
            $scope.category = key;
        };

        $scope.renderResult = function(type, obj) {
            if (type === "racer") {
                return obj.first_name + " " + obj.last_name;
            }

            return obj.name
        };

        $scope.renderUrl = function(type, obj) {
            switch (type) {
                case "tournament":
                    return "#/tournament/" + obj.slug;
                case "track":
                    return "#/track/" + obj.id;
                case "racer":
                    return "#/racer/" + obj.id;
                case "race":
                    return "#/race/" + obj.id;
            }
        };

        Restangular.one("search").get({q: $scope.q}).then(function (response) {
            $scope.result = response.data.plain();
            for (var key in $scope.result){
                if ($scope.result.hasOwnProperty(key)){
                    if ($scope.result[key].length){
                        $timeout(function () {
                            $scope.showSearchResult(key);
                        });
                        return;
                    }
                }
            }
            $scope.category = "Výsledky";
        })
    }]);

    trackie_module.controller("TournamentCreateController", ["$scope", "$location", "Restangular", function($scope, $location, Restangular){
        $scope.tournamentForm = {};

        $scope.createTournament = function(){
            var data = $scope.tournamentForm.data;
            Restangular.all("tournaments").post(data).then(function (response) {
                $location.path("/tournament/" + response.data.id);
            }, function (error) {
                renderFormErrors($("#tournament-form"), error.data, "id_");
            });
        };
    }]);

    trackie_module.controller("TournamentController", ["$scope", "$location", "$routeParams", "Restangular", "djangoAuth", function($scope, $location, $routeParams, Restangular, djangoAuth){
        $scope.render_link = function (grid, row, col) {
            var url = "#/race/" + row.entity.id;
            return '<a href="' + url + '">' + grid.getCellValue(row, col) + '</a>';
        };

        $scope.time = function(grid, row, col){
            var timestamp = row.entity[col.field];
            if (!timestamp) return;
            var time = moment(timestamp).tz(window.timezone);
            return time.format("L LTS");
        };

        $scope.duration_time = function (_, row) {
            var start = moment(row.entity.real_start);
            var end = moment(row.entity.real_end);
            var duration = moment(moment.duration(row.entity.estimated_duration)._data);
            if (start.isValid() && end.isValid()){
                duration = moment(end.diff(start)).utc()
            }
            return duration.format("HH:mm:ss");
        };

        $scope.deleteTournament = function () {
            $scope.tournament.remove().then(function (response) {
                $location.path("/");
            }, function (error) {
                if (error.status.toString()[0] == 4) { //4xx
                    $location.url("/" + error.status + "?from=" + $location.path());
                }
            })
        };

        djangoAuth.authenticationStatus().then(function () {
            $scope.user = djangoAuth.user;
        });

        $scope.grid = {
            paginationPageSizes: [10, 20, 50],
            onRegisterApi: function (gridApi) {
                $scope.gridApi = gridApi;
            },
            columnDefs: [
                {
                    name: "Závod",
                    field: "name",
                    cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.render_link(grid, row, col)"><div>'},
                {
                    name: "Začiatok",
                    field: "start",
                    type: "date",
                    cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.time(grid, row, col)"><div>'},
                {
                    name: "Koniec",
                    field: "end",
                    type: "date",
                    cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.time(grid, row, col)"><div>'},
                {
                    name: "Dĺžka",
                    field: "end",
                    type: "date",
                    cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.duration_time(grid, row, col)"><div>'}
            ]
        };

        Restangular.all("tournaments").one($routeParams.id).get().then(function (response) {
                $scope.tournament = response.data;
                Restangular.allUrl("races", $scope.tournament.races).getList().then(function (response) {
                    $scope.races = response.data;
                    $scope.grid.data = $scope.races.plain();
                })
            }, function (error) {
                if (error.status.toString()[0] == 4) { //4xx
                    $location.url("/" + error.status + "?from=" + $location.path());
                }
            }
        )
    }]);

    trackie_module.controller("TournamentsController", ["$scope", "$location", "$routeParams", "Restangular", function($scope, $location, $routeParams, Restangular){
        $scope.render_link = function (grid, row, col) {
            var column = col.field;
            var url = "";
            switch (column){
                case "name":
                    url = url = "#/tournament/" + row.entity.id;
                    break;
                case "sport.name":
                     url = "#/sports/" + row.entity.sport.slug;
                    break;
            }
            return '<a href="' + url + '">' + grid.getCellValue(row, col) + '</a>';
        };

        $scope.grid = {
            paginationPageSizes: [10, 20, 50],
            onRegisterApi: function (gridApi) {
                $scope.gridApi = gridApi;
            },
            columnDefs: [
                {
                    name: "Šport",
                    field: "sport.name",
                    cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.render_link(grid, row, col)"><div>'},
                {
                    name: "Turnaj",
                    field: "name",
                    cellTemplate:'<div class="ui-grid-cell-contents" data-ng-bind-html="grid.appScope.render_link(grid, row, col)"><div>'}
            ]
        };

        Restangular.all("tournaments").getList().then(function (response) {
                $scope.tournaments = response.data;
                $scope.grid.data = $scope.tournaments.plain();
            }, function (error) {
                if (error.status.toString()[0] == 4) { //4xx
                    $location.url("/" + error.status + "?from=" + $location.path());
                }
            }
        )
    }]);

    trackie_module.controller("TournamentUpdateController", ["$scope", "$location", "$routeParams", "Restangular", function ($scope, $location, $routeParams, Restangular) {
        $scope.updateTournament = function () {
            $scope.tournament = angular.extend($scope.tournament, $scope.tournamentForm.data);
            $scope.tournament.put().then(function (response) {
                $location.path("/tournament/" + response.data.id);
            }, function (error) {
                if (error.status.toString()[0] == 4) { //4xx
                    $location.url("/" + error.status + "?from=" + $location.path());
                }
            });
        };

        Restangular.one("tournaments", $routeParams.id).get().then(function (response) {
            $scope.tournament = response.data;
            $scope.tournament.sport = ""+$scope.tournament.sport.id;
            $scope.tournamentForm.data = response.data.plain();
        }, function (error) {
            if (error.status.toString()[0] == 4) { //4xx
                $location.url("/" + error.status + "?from=" + $location.path());
            }
        });
    }]);

    trackie_module.controller("TypeCreateController", ["$scope", "$location", "Restangular", function ($scope, $location, Restangular) {
        $scope.createType = function () {
            Restangular.all("race-types").post($scope.typeForm.data).then(function (response) {
                $location.path("/race-fields/" + response.data.id);
            }, function (error) {
                renderFormErrors($("#type-form"), error.data, "id_");
            });
        };
    }]);

    trackie_module.controller("TypeController", ["$scope", "$location", "$routeParams", "Restangular", "djangoAuth", function ($scope, $location, $routeParams, Restangular, djangoAuth) {
        $scope.renderValue = function(type){
            switch (type) {
                case "BigIntegerField":
                    return '9223372036854775807';
                case "BooleanField":
                    return 'true';
                case "DateField":
                    return '"1970-01-01"';
                case "DateTimeField":
                    return '"1970-01-01T00:00:00"';
                case "DurationField":
                case "TimeField":
                    return '"15:15:15"';
                case "FloatField":
                    return '645.1554';
                case "IntegerField":
                case "PositiveIntegerField":
                    return '2147483647';
                case "SmallIntegerField":
                case "PositiveSmallIntegerField":
                    return '32767';
                case "TextField":
                    return '"Lorem ipsum"';
                case "URLField":
                    return 'http://localhost/foo/bar.html';
            }
        };

        $scope.deleteType = function(){
            $scope.type.remove().then(function (response) {
                $location.path("/");
            }, function (error) {
                if (error.status.toString()[0] == 4) { //4xx
                    $location.url("/" + error.status + "?from=" + $location.path());
                }
            });
        };

        djangoAuth.authenticationStatus().then(function () {
            $scope.user = djangoAuth.user;
        });

        Restangular.one("race-types", $routeParams.id).get().then(function (response) {
                $scope.type = response.data;
            }, function (error) {
                if (error.status.toString()[0] == 4) { //4xx
                    $location.url("/" + error.status + "?from=" + $location.path());
                }
            }
        )
    }]);

    trackie_module.controller("TypeUpdateController", ["$scope", "$location", "$routeParams", "Restangular", function ($scope, $location, $routeParams, Restangular) {
        $scope.updateType = function () {
            $scope.type = angular.extend($scope.type, $scope.typeForm.data);
            $scope.type.put().then(function (response) {
                $location.path("/race-fields/" + response.data.id);
            }, function (error) {
                if (error.status.toString()[0] == 4) { //4xx
                    $location.url("/" + error.status + "?from=" + $location.path());
                }
            });
        };

        Restangular.one("race-types", $routeParams.id).get().then(function (response) {
            $scope.type = response.data;
            $scope.type.fields = _.map($scope.type.fields, function(item){return String(item.id)});
            $scope.typeForm.data = response.data.plain();
        }, function (error) {
            if (error.status.toString()[0] == 4) { //4xx
                $location.url("/" + error.status + "?from=" + $location.path());
            }
        });
    }]);

}());
