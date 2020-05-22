exports.config = {
    capability : {
        browserName : "chrome",
    },
    chromeDriver: "/Users/sudharsan/Documents/Applications/chromedriver",
    directConnect: true,
    suites : {
        all : ["/Users/sudharsan/Documents/git/selenium-image-sketch/protractor/spec.js"]
    },
    jasmineNodeOpts: {
        defaultTimeoutInterval: 2700000, //45 mins
    },

};
