#
# Requeries networkx and pywebview (pip3 install networkx pywebview)
# References:
#   - https://ipython-books.github.io/64-visualizing-a-networkx-graph-in-the-notebook-with-d3js/

import json
import networkx as nx
import webview
import time

# Load Zachary's Karate Club graph
g = nx.karate_club_graph()

nodes = [{'name': str(i), 'club': g.nodes[i]['club']}
         for i in g.nodes]

links = [{'source': u[0], 'target': u[1]}
         for u in g.edges]

json_graph = json.dumps({
    "nodes": nodes,
    "links": links
})

html = f"""
<body>
    <h1>Live Graph Preview</h1>

    <style>
    .svg-container {{
        display: inline-block;
        margin: 0 auto;
    }}
    .node {{stroke: #fff; stroke-width: 1.5px;}}
    .link {{stroke: #999; stroke-opacity: .6;}}
    </style>
    <div class="svg-container" id="d3-example"></div>

    <script src="https://d3js.org/d3.v3.min.js"></script>
    <script>
    var graph = {json_graph};

    var width = 600, height = 400;
    var color = d3.scale.category10();

    var force = d3.layout.force()
        .charge(-120)
        .linkDistance(30)
        .size([width, height]);

    var svg = d3.select("#d3-example").select("svg")
    if (svg.empty()) {{
        svg = d3.select("#d3-example").append("svg")
            .attr("style", "outline: thin solid black;")  
            .attr("width", width)
            .attr("height", height);
    }}

    force.nodes(graph.nodes)
    .links(graph.links)
    .start();

    var link = svg.selectAll(".link")
    .data(graph.links)
    .enter().append("line")
    .attr("class", "link");

    var node = svg.selectAll(".node")
    .data(graph.nodes)
    .enter().append("circle")
    .attr("class", "node")
    .attr("r", 5)  // radius
    .style("fill", function(d) {{
        // The node color depends on the club.
        return color(d.club);
    }})
    .call(force.drag);

    node.append("title")
        .text(function(d) {{ return d.name; }});

    force.on("tick", function() {{
    link.attr("x1", function(d){{return d.source.x}})
        .attr("y1", function(d){{return d.source.y}})
        .attr("x2", function(d){{return d.target.x}})
        .attr("y2", function(d){{return d.target.y}});

    node.attr("cx", function(d){{return d.x}})
        .attr("cy", function(d){{return d.y}});
    }});
    </script>
</body>
"""

def start(window):
    time.sleep(2)

    result = window.evaluate_js(
        r"""
        var h1 = document.createElement('h1')
        var text = document.createTextNode('Dynamic JS eval test')
        h1.appendChild(text)
        document.body.appendChild(h1)
        """
    )

window = webview.create_window('Graph', html=html, on_top=True) #width=800, height=800)
webview.start(func=start, debug=True, args=window)