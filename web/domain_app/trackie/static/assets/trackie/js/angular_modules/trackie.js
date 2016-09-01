(function () {
    "use strict";
    var trackie_module = angular.module("trackie", ["ngRoute", "ngResource", "restangular"])
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
        }]);
        // .config(["$routeProvider", "$locationProvider", function ($routeProvider, $locationProvider) {
        //     $routeProvider.when("/Book/:bookId", {
        //         templateUrl: "book.html",
        //         controller: "BookCtrl",
        //         controllerAs: "book"
        //     }).when("/Book/:bookId/ch/:chapterId", {
        //         templateUrl: "chapter.html",
        //         controller: "ChapterCtrl",
        //         controllerAs: "chapter"
        //     });
        //
        //     $locationProvider.html5Mode(true);
        // }]);

    trackie_module.controller("mainController", ["$scope", "Restangular", function ($scope, Restangular) {
        $scope.login = function () {
            Restangular.all("auth").customPOST({"username": "admin", "password": "root"}, "login");
        };
    }]);
}());
