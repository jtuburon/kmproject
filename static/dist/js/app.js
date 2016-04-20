var app = angular.module('plunker', ['ngTagsInput']);

app.controller('MainCtrl', function($scope, $http) {
  $scope.tags = [
    { name: "Brazil", flag: "Brazil.png" },
    { name: "Italy", flag: "Italy.png" },
    { name: "Spain", flag: "Spain.png" },
    { name: "Germany", flag: "Germany.png" },
  ];
  
  $scope.loadCountries = function($query) {
    return $http.get('countries.json', { cache: true}).then(function(response) {
      var countries = response.data;
      return countries.filter(function(country) {
        return country.name.toLowerCase().indexOf($query.toLowerCase()) != -1;
      });
    });
  };
});