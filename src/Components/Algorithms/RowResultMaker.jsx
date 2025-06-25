import React from "react";

const RowResultMaker = ({ result, index_arr }) => {
  return (
    <>
      {result.map((item, rowIndex) => {
        const lastEle = item[item.length - 1];

        return (
          <tr
            key={rowIndex}
            className="transition-transform duration-500 ease-out animate-fadeInUp"
            style={{
              animationDelay: `${rowIndex * 0.2}s`,
              animationFillMode: "both",
            }}
          >
            {item.map((cell, cellIndex) => {
              const isResultCol = cellIndex === item.length - 1;
              const isHighlight = cellIndex === index_arr[rowIndex] + 1;

              const baseClasses =
                "border px-4 py-2 text-center font-medium transition duration-300 ease-in-out";

              if (!isHighlight) {
                const bgColor = isResultCol
                  ? lastEle === "HIT"
                    ? "bg-[#7C99AC]"
                    : "bg-[#FFCDDD]"
                  : "bg-[#2d3748]";

                const textColor = isResultCol ? "text-black" : "text-white";
                const borderColor = isResultCol ? "border-black" : "border-gray-600";

                return (
                  <td
                    key={cellIndex}
                    className={`${baseClasses} ${bgColor} ${textColor} ${borderColor}`}
                  >
                    {cell}
                  </td>
                );
              } else {
                const highlightColor =
                  lastEle === "HIT"
                    ? "hover:bg-green-400 bg-green-500/80 text-white"
                    : "bg-red-600 text-white";

                return (
                  <td
                    key={cellIndex}
                    className={`${baseClasses} ${highlightColor} border-gray-700 hover:scale-105`}
                  >
                    {cell}
                  </td>
                );
              }
            })}
          </tr>
        );
      })}
    </>
  );
};

export default RowResultMaker;
