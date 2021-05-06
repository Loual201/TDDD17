import React, { useEffect, useState } from 'react';
import * as d3 from 'd3';
import { sankey, sankeyLinkHorizontal, sankeyLeft } from 'd3-sankey';
import { scaleThreshold } from 'd3-scale';

const SankeyNode = ({ name, x0, x1, y0, y1, color }) => {
  return (
    <rect
      x={x0}
      y={y0}
      width={x1 - x0}
      height={Math.max(y1 - y0, 3)}
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
      strokeOpacity: '.5',
      stroke: color,
      strokeWidth: Math.max(1, link.width),
    }}
  />
);

const MysteriousSankey = ({ data, width, height, colorRange }) => {
  const [nodes, setNodes] = useState([]);
  const [links, setLinks] = useState([]);

  var uniqueNodes = [];
  var uniquelinks = [];

  var colorDomain = [1, 10, 20, 50, 100, 400, 700];

  useEffect(() => {
    data.map((d) => {
      setNodes((nodes) => [...nodes, { name: d.source, count: d.count }]);
      setNodes((nodes) => [...nodes, { name: d.target, count: d.count }]);

      setLinks((links) => [
        ...links,
        { source: d.source, target: d.target, value: d.value, count: d.count },
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

  // Gör om noderna till objekt
  var nodesAsObjeccts = [];
  uniqueNodes.map((n, i) => {
    nodesAsObjeccts = [...nodesAsObjeccts, { name: n }];
  });

  uniquelinks = links;

  if (uniqueNodes.length != 0 && uniquelinks.length != 0) {
    sankey()
      .nodeWidth(15)
      .nodePadding(10)
      .nodeAlign(sankeyLeft)
      .extent([
        [1, 1],
        [width - 1, height - 5],
      ])({ nodes: nodesAsObjeccts, links: uniquelinks });
  }

  var maxCount = Math.max.apply(
    Math,
    uniquelinks.map(function (link) {
      return link.count;
    })
  );

  var minCount = Math.min.apply(
    Math,
    uniquelinks.map(function (link) {
      return link.count;
    })
  );

  function palette(min, max) {
    var col = scaleThreshold().range(colorRange).domain(colorDomain);
    return col;
  }

  var colorScheme = palette(minCount, maxCount);

  const linkColor = (l) => {
    return colorScheme(l.count);
  };

  return (
    <>
      <g style={{ mixBlendMode: 'multiply' }}>
        {nodesAsObjeccts.map((node, i) => (
          <SankeyNode {...node} color={'#808080'} key={node.name} />
        ))}
        {uniquelinks.map((link, i) => (
          <SankeyLink link={link} color={linkColor(link)} />
        ))}
      </g>
    </>
  );
};

export default MysteriousSankey;
