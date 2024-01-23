"use client";

export default function WritePassword({ elements, submitPassword }) {
  const password = new Array(20).fill("");
  return (
    <div>
      <form
        className="flex flex-col justify-center items-center h-screen"
        onSubmit={(e) => {
          submitPassword(e, password.join(""));
        }}
      >
        <label className="text-4xl mb-10">Wpisz litery hasła:</label>
        <div className="w-3/4 ">
          {Array.from({ length: 20 }, (_, index) => {
            const toWrite = elements.includes(index.toString());
            return (
              <input
                type="text"
                className="rounded-full border-2 border-yellow-400"
                id={index}
                key={index}
                style={{
                  textAlign: "center",
                  width: "3vw",
                  height: "4vw",
                  margin: 5,
                  color: "black",
                  border: "solid 2px rgb(245 158 11)",
                  backgroundColor: toWrite ? "white" : "gray",
                }}
                readOnly={toWrite ? false : true}
                onChange={(e) => {
                  e.target.value = e.target.value.slice(0, 1);
                  password[Number(index)] = e.target.value;
                }}
              />
            );
          })}
        </div>
        <input
          className="bg-yellow-400 px-10 py-5 rounded-full mt-5 drop-shadow-lg hover:bg-yellow-600 text-xl"
          type="submit"
          value="Zaloguj"
        />
      </form>
    </div>
  );
}
