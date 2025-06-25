import React from "react";
import Chart from "react-google-charts";

const PieChart = ({ hit, fault }) => {
  const total = hit + fault;
  const pieData = [
    ["Page Sequence", "Hit/Fault"],
    ["Hit", hit],
    ["Fault", fault],
  ];

  const pieOptions = {
    title: "Hit Vs Fault Comparison",
    is3D: true,
    backgroundColor: "#1a202c",
    titleTextStyle: {
      color: "#fff",
      fontSize: 24,
    },
    pieSliceTextStyle: {
      color: "black",
      fontSize: 24,
    },
    slices: {
      0: { color: "#7C99AC" }, // Hit
      1: { color: "#FFCDDD" }, // Fault
    },
    legend: {
      textStyle: { color: "#fff", fontSize: 16 },
    },
    tooltip: { textStyle: { fontSize: 16 } },
  };

  const tableData = [
    {
      label: "Hit",
      value: hit,
      color: "#7C99AC",
      percentage: ((hit / total) * 100).toFixed(2) + "%",
    },
    {
      label: "Fault",
      value: fault,
      color: "#FFCDDD",
      percentage: ((fault / total) * 100).toFixed(2) + "%",
    },
  ];

  return (
    <div className="w-full mt-8 mb-5 flex flex-col items-center justify-center px-4">
      <h2 className="mb-6 text-5xl font-semibold text-white text-center drop-shadow-lg transition-all duration-500 ease-in-out hover:text-[#FFCDDD]">
        Pie Chart
      </h2>

      <div className="rounded-2xl shadow-2xl overflow-hidden transform transition duration-500 hover:scale-105 hover:shadow-[#7C99AC]/50 bg-[#2d3748] p-4">
        <Chart
          width={"900px"}
          height={"500px"}
          chartType="PieChart"
          loader={<div className="text-white text-xl animate-pulse">Loading Chart...</div>}
          data={pieData}
          options={pieOptions}
          rootProps={{ "data-testid": "3" }}
        />
      </div>

      {/* Summary Table */}
      <div className="w-full max-w-2xl mt-8">
        <h3 className="text-2xl font-semibold text-white mb-4 text-center">Chart Summary</h3>
        <table className="w-full table-auto text-center border-collapse rounded-xl overflow-hidden shadow-lg">
          <thead className="bg-gray-800 text-white">
            <tr>
              <th className="py-2 px-4 border border-gray-700">Label</th>
              <th className="py-2 px-4 border border-gray-700">Value</th>
              <th className="py-2 px-4 border border-gray-700">Percentage</th>
              <th className="py-2 px-4 border border-gray-700">Color</th>
            </tr>
          </thead>
          <tbody className="text-white">
            {tableData.map((item, index) => (
              <tr
                key={index}
                className="transition-colors duration-300 hover:bg-gray-700"
              >
                <td className="py-2 px-4 border border-gray-700">{item.label}</td>
                <td className="py-2 px-4 border border-gray-700">{item.value}</td>
                <td className="py-2 px-4 border border-gray-700">{item.percentage}</td>
                <td className="py-2 px-4 border border-gray-700">
                  <span
                    className="inline-block w-4 h-4 rounded-full"
                    style={{ backgroundColor: item.color }}
                  ></span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PieChart;
