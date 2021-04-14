import React, { useEffect, useState, useRef } from 'react';
import * as d3 from 'd3';

import inputData from './dataset.csv';

import Sankey from './sankey';

const App = () => {
  const [data, setData] = useState(null);
  const [width, setWidth] = useState(0);
  const [height, setHeight] = useState(0);

  const svgRef = useRef();

  const measureSVG = () => {
    const { width, height } = svgRef.current.getBoundingClientRect();

    setWidth(width);
    setHeight(height);
  };

  useEffect(() => {
    d3.csv(inputData).then(
      (d) => {
        setData(d);
      },
      [inputData]
    );

    measureSVG();
    window.addEventListener('resize', measureSVG);
  }, []);

  useEffect(() => {
    window.removeEventListener('resize', measureSVG);
  });

  return (
    <div className="App">
      <h1>Let's build a Sankey diagram</h1>
      <h2>#ReactVizHoliday Day 11</h2>
      <svg width="100%" height="600" ref={svgRef}>
        {data && <Sankey data={data} width={width} height={height} />}
      </svg>
    </div>
  );
};

export default App;
