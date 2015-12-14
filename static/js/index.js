var nodeset = new Set()
var nodes = []
var clinks = []
var links = []

var width = document.documentElement.clientWidth,
    height = document.documentElement.clientHeight;
var x = d3.scale.linear().domain([0, width]).range([0, width]);
var y = d3.scale.linear().domain([0, height]).range([height, 0]);
var svg = d3.select("body").append("svg").attr("width", width).attr("height", height).append("g");
var link = svg.selectAll(".link"),
    node = svg.selectAll(".node");
svg.append("rect").attr("class", "overlay").attr("width", width).attr("height", height);
var node_drag = d3.behavior.drag().on("dragstart", dragstart).on("drag", dragmove).on("dragend", dragend);

function dragstart(b, a) {
    force.stop();
    event.stopPropagation()
}

function dragmove(b, a) {
    b.px += d3.event.dx;
    b.py -= d3.event.dy;
    b.x += d3.event.dx;
    b.y -= d3.event.dy;
    tick()
}

function dragend(b, a) {
    b.fixed = true;
    tick();
    force.resume()
}


$(document).ready(function() {
    $.ajax({
            url: './nm1670029.json',
            type: 'GET',
            dataType: 'json',
        })
        .done(function(data) {

            for (k in data) {
                if (data.hasOwnProperty(k)) {
                    nodeset.add(k); //电影id
                    data[k].artists.forEach(function(x) {
                        nodeset.add(x.actorId); //演员id
                        clinks.push({
                            source: k,
                            target: x.actorId
                        });
                    })
                }
            }

            nodeset.forEach(function(x) {
                nodes.push({
                    name: x
                })
            });
            clinks.forEach(function(x) {
                links.push({
                    source: indexOfName(x.source),
                    target: indexOfName(x.target)
                })
            });
            restart();
        })
        .fail(function() {
            console.log("error");
        })
        .always(function() {
            console.log("complete");
        });

});

function indexOfName(name) {
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].name === name) return i;
    }
    return -1;
}


function restart() {
    var force = d3.layout.force()
        .nodes(nodes) //指定节点数组
        .links(links) //指定连线数组
        .size([width, height]) //指定作用域范围
        .linkDistance(150) //指定连线长度
        .charge([-400]); //相互之间的作用力
    force.start();

    var color = d3.scale.category20();
    svg.selectAll(".link").remove();
    svg.selectAll(".node").remove();
    link = svg.selectAll(".link").data(links).enter().append("line").attr("class", "link");
    node = svg.selectAll(".node").data(nodes).enter().append("circle").attr("r",10).style("fill",function(d,i){
         return color(i);
     })
     .call(force.drag);  //使得节点能够拖动
    text = svg.selectAll("text")
        .data(nodes)
        .enter()
        .append("text")
        .style("fill", "black")
        .attr("dx", 20)
        .attr("dy", 8)
        .text(function(d) {
            return d.name;
        });
    force.on("tick", function() {
        node.attr("transform", function(a) {
            return "translate(" + x(a.x) + "," + y(a.y) + ")"
        });
        link.attr("x1", function(a) {
            return x(a.source.x)
        }).attr("y1", function(a) {
            return y(a.source.y)
        }).attr("x2", function(a) {
            return x(a.target.x)
        }).attr("y2", function(a) {
            return y(a.target.y)
        })
        text.attr("x", function(d) {
                return x(d.x);
            })
            .attr("y", function(d) {
                return y(d.y);
            });
    })
}
