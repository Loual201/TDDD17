import React, { useEffect, useState, useRef } from 'react';
import * as d3 from 'd3';
import './App.css';
import { Colorscale } from 'react-colorscales';

// Choose which data to visualize
//import inputData from './collected_data/data.csv';
//import inputData from './collected_data/filtered_data.csv';
import inputData from './collected_data/top_txs_data.csv';

import Sankey from './sankey';

const App = () => {
  const [data, setData] = useState(null);
  const [width, setWidth] = useState(0);
  const [height, setHeight] = useState(0);
  var colorRange = [
    '#003f5c',
    '#374c80',
    '#7a5195',
    '#bc5090',
    '#ef5675',
    '#ff764a',
    '#ffa600',
  ];
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
      <h1>Bitcoin flow</h1>
      <svg width="90%" height="600" ref={svgRef}>
        {data && (
          <Sankey
            data={data}
            width={width}
            height={height}
            colorRange={colorRange}
          />
        )}
      </svg>
      <Colorscale colorscale={colorRange} width={150} />
    </div>
  );
};

export default App;
