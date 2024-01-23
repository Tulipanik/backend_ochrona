import * as React from "react";

export default function PasswordMeterInput({ password, setPassword }) {
  const [entropy, setEntropy] = React.useState(0);

  function calculateEntropy(text) {
    let leng = 0;
    let stat = {};

    for (let i = 0; i < text.length; i++) {
      let symb = text[i];
      leng++;

      if (stat.hasOwnProperty(symb)) {
        stat[symb]++;
      } else {
        stat[symb] = 1;
      }
    }

    let H = 0.0;

    for (let znak in stat) {
      if (stat.hasOwnProperty(znak)) {
        let p_i = stat[znak] / leng;
        H -= p_i * Math.log2(p_i);
      }
    }

    return H;
  }

  React.useEffect(() => {
    const calculatedEntropy = calculateEntropy(password);
    setEntropy(calculatedEntropy);
  }, [password]);

  const getEntropyColorClass = () => {
    if (entropy <= 2.5) {
      return "bg-red-400";
    } else if (entropy <= 3.7) {
      return "bg-yellow-400";
    } else {
      return "bg-green-500";
    }
  };

  return (
    <div className="flex w-1/6">
      {Array.from({ length: 5 }, (_, index) => (
        <div key={index} className="w-1/5 px-1">
          <div
            className={`h-2 rounded-xl transition-colors ${
              entropy ? getEntropyColorClass() : "bg-gray-200"
            }`}
          ></div>
        </div>
      ))}
    </div>
  );
}
