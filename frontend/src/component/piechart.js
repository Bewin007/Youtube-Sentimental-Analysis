// import React from 'react';
// import { PieChart } from 'react-minimal-pie-chart';



// const ResponsivePieChart = ({data}) => {
//   console.log(data)
//   const [windowWidth, setWindowWidth] = React.useState(window.innerWidth);

//   React.useEffect(() => {
//     const handleResize = () => setWindowWidth(window.innerWidth);
//     window.addEventListener('resize', handleResize);
//     return () => window.removeEventListener('resize', handleResize);
//   }, []);

//   const chartSize = Math.min(windowWidth * 0.8, 500); // set max width to 500

//   return (
//     <div style={{ width: '100%', maxWidth: chartSize }}>
//       <PieChart
//         data={data}
//         lineWidth={100}
//         label={({ dataEntry }) => dataEntry.title}
//         labelStyle={{
//           fontSize: '5px',
//           fontFamily: 'sans-serif',
//           fill: '#fff',
//         }}
//         animate
//       />
//     </div>
//   );
// };

// export default ResponsivePieChart;
import React from 'react';
import { PieChart } from 'react-minimal-pie-chart';

const ResponsivePieChart = ({ data }) => {
  console.log(data);
  const [windowWidth, setWindowWidth] = React.useState(window.innerWidth);

  React.useEffect(() => {
    const handleResize = () => setWindowWidth(window.innerWidth);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const chartSize = Math.min(windowWidth * 0.8, 500); // set max width to 500

  return (
    <div style={{ width: '100%', maxWidth: chartSize }}>
      <PieChart
        data={data.filter(entry => entry.value !== 0)} // Filter out entries with value 0
        lineWidth={100}
        label={({ dataEntry }) => (dataEntry.value !== 0 ? dataEntry.title : '')} // Show label only if value is not 0
        labelStyle={{
          fontSize: '5px',
          fontFamily: 'sans-serif',
          fill: '#fff',
        }}
        animate
      />
    </div>
  );
};

export default ResponsivePieChart;
