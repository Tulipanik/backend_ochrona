export default function Table({ tableData }) {
  return (
    <table className="table-flex w-screen my-10 border-collapse border border-gray-300 [&_th]:bg-yellow-400 [&_th]:border [&_th]:border-gray-300 [&_td]:border [&_td]:border-gray-300 [&_tr]:border [&_tr]:border-gray-300">
      <thead>
        <tr>
          <th>To</th>
          <th>amount</th>
          <th>Title</th>
          <th>Adress</th>
        </tr>
      </thead>
      <tbody>
        {tableData.map((elem, index) => {
          return (
            <tr key={index}>
              <td>{elem.to_account}</td>
              <td>{elem.amount}</td>
              <td>{elem.title}</td>
              <td>{elem.receiver_data}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
