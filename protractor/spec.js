var plot  = require("../dict.json");
var fs = require("fs");
describe("add custom urls to firebase", function () {


    beforeAll(function () {
        browser.ignoreSynchronization = true;
        //browser.get("https://console.firebase.google.com/u/1/project/boomi-catalog-and-prep-conc/performance/app/web:ZmNhOTgwNWEtZDJjNS00NjVmLWFkY2YtYjk5ODkzM2MwZGQ1/network");
         browser.get("https://vrobbi-nodedrawing.herokuapp.com/");
        //$("body").click();
        //
        // element(by.cssContainingText("a","Start drawing")).click();
        // browser.sleep(1000);
    });


    xit("draw thr plot", function () {
        var actionString ="";
        plot.forEach(async function (p) {
            actionString = "";
            var actionChain = browser.actions();
            actionString = `browser.actions()`;
            p.forEach(function (c, i) {
                actionChain = actionChain.mouseMove($("body"), { x: c.x -0, y: c.y -0 });
                actionString = actionString + `.mouseMove($("body"), { x: ${c.x -0}, y: ${c.y -0} })`
                if((i+1)%2 ==0) {
                    actionChain = actionChain.mouseUp();
                    actionString = actionString + ".mouseUp()"
                } else {
                    actionChain = actionChain.mouseDown()
                    actionString = actionString + ".mouseDown()"
                }
            })

            await actionChain.mouseUp().perform();
            actionString = actionString + ".mouseUp().perform()"
            console.log(actionString);
        });
        browser.sleep(100000);
    });

    var xDiff = 200;
    var yDiff = -100;

    it("drao", async function () {
        var actions = [];
        for(var i=0;i < plot.length ;i++) {
            var actionsString = "";
            var action = browser.actions()
                .mouseMove($("body"), { x: plot[i][0].x - xDiff , y: plot[i][0].y - yDiff})
                .mouseDown();

            actionsString = ` browser.actions().mouseMove($("body"), { x: ${plot[i][0].x - xDiff} , y: ${plot[i][0].y - yDiff }}).mouseDown()`;
            for(j=1;j<plot[i].length; j++) {
               //action = action.mouseMove($("body"), {x: plot[i][j].x  - 300 , y: plot[i][j].y+ 200 }).mouseUp().mouseDown();
                actionsString = actionsString+ `.mouseMove($(\"body\"), { x: ${plot[i][j].x - xDiff} , y: ${plot[i][j].y - yDiff}})`
            }
           // await action.mouseUp().perform();
            actionsString = actionsString+ ".mouseUp().perform()";
            actions.push(actionsString)
        }


        //actions.sort(() => Math.random() - 0.5);
        fs.writeFileSync("actions3.json", JSON.stringify(actions, null, 2));
    })
    
});

//browser.ignoreSynchronization = true;var a = require("/Users/sudharsan/Documents/git/selenium-image-sketch/actions3.json");browser.get("https://vrobbi-nodedrawing.herokuapp.com/");
