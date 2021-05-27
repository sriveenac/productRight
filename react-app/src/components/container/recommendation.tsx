import styles from './recommendation.css';
import { useState, useEffect } from 'react';
import { Table } from 'antd'

export default function Recommendation() {
    // Recommendation data from back end (table-like json)
    const [specNearestItems, setSpecNearestItems] = useState({});
    const [dataSource, setDataSource] = useState([]);
    const [columns, setColumns] = useState([]);
    
    // Get table-like json from back-end
    useEffect(()=>{
      fetch('/api/nearest-items').then(res => res.json()).then(data => {
        setSpecNearestItems(data);

        // Convert table-like json data to antd Table data
        let ds = [];
        for (const key in data) {
          let newObject = {
            ...data[key],
            key: key,
          };
          ds.push(newObject);
        }
        setDataSource(ds);

        // Extract column names for antd Table columns
        // TODO: if there is no entry in data
        let cols = [];
        for (const attribute in data[0]) {
          let newObject = {
            key: attribute,
            dataIndex: attribute,
            title: attribute,
          };
          cols.push(newObject);
        }
        setColumns(cols);
      });
    }, []);

    return (
        <div>
            <h1 className={styles.title}>Recommendation</h1>
            <table width='100%'>
              <tr>
                <td width='20%'>Please input your item:</td>
                <td width='80%'>
                  <Table dataSource={dataSource} columns={columns}></Table>
                </td>
              </tr>
            </table>
        </div>
    );
}