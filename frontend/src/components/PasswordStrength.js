import * as React from "react";
import Stack from "@mui/joy/Stack";
import Input from "@mui/joy/Input";
import LinearProgress from "@mui/joy/LinearProgress";
import Typography from "@mui/joy/Typography";
import Key from "@mui/icons-material/Key";

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
    <Stack
      spacing={0.5}
      sx={{
        "--hue": Math.min(value.length * 10, 120),
      }}
    >
      <Input
        type="password"
        placeholder="Type in here…"
        startDecorator={<Key />}
        value={value}
        onChange={(event) => setValue(event.target.value)}
      />
      <LinearProgress
        determinate
        size="sm"
        value={Math.min((value.length * 100) / minLength, 100)}
        sx={{
          bgcolor: "background.level3",
          color: "hsl(var(--hue) 80% 40%)",
        }}
      />
      <Typography
        level="body-xs"
        sx={{ alignSelf: "flex-end", color: "hsl(var(--hue) 80% 30%)" }}
      >
        {calculateEntropy(password) < 3 && "Very weak"}
        {calculateEntropy(password) >= 3 &&
          calculateEntropy(password) < 6 &&
          "Weak"}
        {calculateEntropy(password) >= 6 &&
          calculateEntropy(password) < 10 &&
          "Strong"}
        {calculateEntropy(password) >= 10 && "Very strong"}
      </Typography>
    </Stack>
  );
}
