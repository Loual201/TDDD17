import React, { useEffect, useState } from 'react';
import * as d3 from 'd3';
import { sankey, sankeyLinkHorizontal } from 'd3-sankey';
import chroma from 'chroma-js';

const SankeyNode = ({ name, x0, x1, y0, y1, color }) => (
  <rect x={x0} y={y0} width={x1 - x0} height={y1 - y0} fill={color}>
    <title>{name}</title>
  </rect>
);

const SankeyLink = ({ link, color }) => (
  <path
    d={sankeyLinkHorizontal()(link)}
    style={{
      fill: 'none',
      strokeOpacity: '.3',
      stroke: color,
      strokeWidth: Math.max(1, link.width),
    }}
  />
);

const MysteriousSankey = ({ data, width, height }) => {
  // console.log(data);
  const [nodes, setNodes] = useState([]);
  const [links, setLinks] = useState([]);
  const [graph, setGraph] = useState({ nodes: [], links: [] });
  var uniqueNodes = [];
  var uniquelinks = [];
  
  useEffect(() => {
    data.map((d) => {
      setNodes((nodes) => [...nodes, { name: d.source }]);
      setNodes((nodes) => [...nodes, { name: d.target }]);

      setLinks((links) => [
        ...links,
        { source: d.source, target: d.target, value: d.value},
      ]);
    });
  }, []);
  
  // Ta ut alla unika noder
  nodes.map((n) => {
    if (!uniqueNodes.includes(n.name)) {
      uniqueNodes = [...uniqueNodes, n.name];
      //console.log("uniqueNodes")
    }
  });

  // Skapa länkar mellan nodernas indexes
  links.map((link) => {
    link.source = uniqueNodes.indexOf(link.source);
    link.target = uniqueNodes.indexOf(link.target);

  });

  //setGraph((g) => ({ nodes: uniqueNodes, links: [] }));
  //console.log(uniqueNodes)
  var nodesAsObjeccts= []
  uniqueNodes.map((n) => {
    nodesAsObjeccts = [...nodesAsObjeccts,{name:n}];
  });

  uniquelinks = links
  //console.log(uniqueNodes)
  //sankey().nodes(uniqueNodes).links(uniquelinks).layout
  
    if(uniqueNodes.length != 0 && uniquelinks.length != 0){
          const { n_nodes, _n_links } = sankey()
        .nodeWidth(15)
        .nodePadding(10)
        //.nodeAlign('justify') TODO: Fix Left alignment
        .extent([
          [1, 1],
          [width - 1, height - 5],
        ])({ nodes: nodesAsObjeccts, links: uniquelinks });
      }
    

  //console.log('nodes');
  //console.log(nodes);
  const color = chroma.scale('Set3').classes(nodesAsObjeccts.length);
  const colorScale = d3.scaleLinear().domain([0, nodesAsObjeccts.length]).range([0, 1]);

  return (
    <g style={{ mixBlendMode: 'multiply' }}>
       {nodesAsObjeccts.map((node, i) => (
        <SankeyNode
          {...node}
         color={color(colorScale(i)).hex()}
          key={node.name}
        />
      ))}
      {uniquelinks.map((link, i) => (
        <SankeyLink
          link={link}
          color={color(colorScale(link.source.index)).hex()}
        />
      ))}
    </g>
  );
};

export default MysteriousSankey;
