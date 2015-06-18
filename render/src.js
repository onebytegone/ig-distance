$(function(){

$.getJSON("../data/summary.json", function(json) {
   var data = _.first(_.values(json));

   var nodes = _.map(_.keys(data), function(username) {
      return {
         'data': {
            'id': username
         }
      }
   })

   var edgeLabelTemplate = _.template("<%= like %>, <%= comment %>, <%= at %>");

   var edges = _.flatten(_.map(data, function(fields, user) {
      return _.map(_.keys(_.first(_.values(fields))), function(key) {
         return {
            'data': {
               'id': user + '-' + key,
               'weight': 1,
               'source': user,
               'target': key,
               'follow': fields['follows'][key] ? 1 : 0,
               'label': edgeLabelTemplate({
                  'like': fields['likesToward'][key],
                  'comment': fields['commentsOnPosts'][key],
                  'at': fields['commentsToward'][key]
               })
            }
         }
      });
   }))

   buildGraph(nodes, edges)
});

function buildGraph(nodes, edges) {
   var cy = cytoscape({
      container: document.getElementById('graph'),

      style: cytoscape.stylesheet()
         .selector('node')
            .css({
               'content': 'data(id)'
            })
         .selector('edge')
            .css({
               'target-arrow-shape': 'triangle',
               'width': 4,
               'line-color': '#ddd',
               'target-arrow-color': '#ddd',
               'target-arrow-color': '#ddd',
               'content': 'data(label)'
            })
         .selector('edge[follow = 0]')
            .css({
               'line-style': 'dashed'
            })
         .selector('.highlighted')
            .css({
               'background-color': '#61bffc',
               'line-color': '#61bffc',
               'target-arrow-color': '#61bffc',
               'transition-property': 'background-color, line-color, target-arrow-color',
               'transition-duration': '0.5s'
            }),

      elements: {
         'nodes': nodes,
         'edges': edges
      },

      layout: {
         name: 'breadthfirst',
         directed: true,
         roots: '#a',
         padding: 10
      }
   });
}




}); // on dom ready
