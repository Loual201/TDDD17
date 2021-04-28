import React, { useEffect, useState } from 'react';
import * as d3 from 'd3';
import { sankey, sankeyLinkHorizontal, sankeyLeft } from 'd3-sankey';
import chroma from 'chroma-js';

const SankeyNode = ({ name, x0, x1, y0, y1, color }) => {
  console.log(name);
  // height ska vara y1-y0
  return (
    <rect
      x={x0}
      y={y0}
      width={x1 - x0}
      height={Math.max(y1 - y0, 1)}
      fill={color}
    >
      <title>{name}</title>
    </rect>
  );
};

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
  const [nodes, setNodes] = useState([]);
  const [links, setLinks] = useState([]);

  var uniqueNodes = [];
  var uniquelinks = [];

  useEffect(() => {
    data.map((d) => {
      setNodes((nodes) => [...nodes, { name: d.source }]);
      setNodes((nodes) => [...nodes, { name: d.target }]);

      setLinks((links) => [
        ...links,
        { source: d.source, target: d.target, value: d.value },
      ]);
    });
  }, []);

  // Ta ut alla unika noder
  nodes.map((n) => {
    if (!uniqueNodes.includes(n.name)) {
      uniqueNodes = [...uniqueNodes, n.name];
    }
  });

  // Skapa länkar mellan nodernas indexes
  links.map((link) => {
    link.source = uniqueNodes.indexOf(link.source);
    link.target = uniqueNodes.indexOf(link.target);
  });

  var nodesAsObjeccts = [];
  uniqueNodes.map((n) => {
    nodesAsObjeccts = [...nodesAsObjeccts, { name: n }];
  });

  uniquelinks = links;

  if (uniqueNodes.length != 0 && uniquelinks.length != 0) {
    // console.log(sankey().nodeAlign('left'));
    console.log(sankey());
    const { n_nodes, _n_links } = sankey()
      .nodeWidth(15)
      .nodePadding(10)
      .nodeAlign(sankeyLeft) // TODO: Fix Left alignment
      .extent([
        [1, 1],
        [width - 1, height - 5],
      ])({ nodes: nodesAsObjeccts, links: uniquelinks });
  }

  // const color = chroma.scale('Set3').classes(nodesAsObjeccts.length);
  //const color = chroma.scale('RdPu').classes(nodesAsObjeccts.length);
  const color = chroma.random(); //.classes(nodesAsObjeccts.length);

  const colorScale = d3
    .scaleLinear()
    .domain([0, nodesAsObjeccts.length])
    .range([1, 0]);

  return (
    <g style={{ mixBlendMode: 'multiply' }}>
      {nodesAsObjeccts.map((node, i) => (
        <SankeyNode {...node} color={chroma.random()} key={node.name} />
      ))}
      {uniquelinks.map((link, i) => (
        <SankeyLink link={link} color={chroma.random()} />
      ))}
    </g>
  );
};

export default MysteriousSankey;
