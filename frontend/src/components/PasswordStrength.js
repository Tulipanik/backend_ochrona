import * as React from "react";

export default function PasswordMeterInput({ password }) {
  const [value, setValue] = React.useState("");
  const minLength = 8;

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

  return (
    <template x-for="(v,i) in 5">
      <div class="w-1/5 px-1">
        <div class="h-2 rounded-xl transition-colors"></div>
      </div>
    </template>
  );
}
