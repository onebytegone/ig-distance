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

   var edgeLabelTemplate = _.template("<%= like %>, <%= comment %>, <%= at %>, <%= commentRatio %>");

   var edges = _.flatten(_.map(data, function(fields, user) {
      return _.map(_.keys(_.first(_.values(fields))), function(key) {
         return {
            'data': {
               'id': user + '-' + key,
               'weight':
                  (fields['likesToward'][key] * 0.3
                  + fields['commentsOnPosts'][key]
                  + fields['commentsToward'][key]).toFixed(2),
               'source': user,
               'target': key,
               'follow': fields['follows'][key] ? 1 : 0,
               'eventCount': fields['likesToward'][key] + fields['commentsOnPosts'][key] + fields['commentsToward'][key],
               'label': edgeLabelTemplate({
                  'like': fields['likesToward'][key],
                  'comment': fields['commentsOnPosts'][key],
                  'at': fields['commentsToward'][key],
                  'commentRatio':  fields['commentsToward'][key]/fields['numOfCommentsMade']
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
               'background-color': '#B6B6B6',
               'content': 'data(id)'
            })
         .selector('edge')
            .css({
               'target-arrow-shape': 'triangle',
               'width': 4,
               'line-color': '#B6B6B6',
               'target-arrow-color': '#B6B6B6',
               'content': 'data(weight)',
               'z-index': 10
            })
         .selector('edge[follow = 0]')
            .css({
               'line-style': 'dashed'
            })
         .selector('edge[eventCount = 0]')
            .css({
               'line-color': '#eee',
               'target-arrow-color': '#eee',
               'content': ''
            })
         .selector('.highlighted')
            .css({
               'background-color': '#448AFF',
               'line-color': '#448AFF',
               'target-arrow-color': '#448AFF'
            })
         .selector('edge.outgoing, edge.incoming')
            .css({
               'font-weight': 'bold',
               'font-size': '1.5em'
            })
         .selector('.outgoing')
            .css({
               'line-color': '#448AFF',
               'target-arrow-color': '#448AFF',
               'z-index': 20
            })
         .selector('.incoming')
            .css({
               'line-color': '#E64A19',
               'target-arrow-color': '#E64A19',
               'z-index': 20
            })
         .selector('.outgoing[eventCount = 0]')
            .css({
               'background-color': '#AAF0FF',
               'line-color': '#AAF0FF',
               'target-arrow-color': '#AAF0FF',
               'z-index': 15
            })
         .selector('.incoming[eventCount = 0]')
            .css({
               'background-color': '#FFB07F',
               'line-color': '#FFB07F',
               'target-arrow-color': '#FFB07F',
               'z-index': 15
            }),

      elements: {
         'nodes': nodes,
         'edges': edges
      },

      layout: {
         name: 'circle',
         padding: 30
      }
   });

   cy.nodes().on("click", function(event){
      var removeClass = function (classname) {
         _.each(cy.$('.'+classname), function(element) {
            element.removeClass(classname);
         });
      };
      removeClass('highlighted');
      removeClass('outgoing');
      removeClass('incoming');

      var addClass = function (nodes, classname) {
         _.each(nodes, function(element) {
            element.addClass(classname);
         });
      };

      var node = event.cyTarget;
      node.addClass('highlighted');
      addClass(node.incomers(), 'incoming');
      addClass(node.outgoers(), 'outgoing');
   });
}

}); // on dom ready
