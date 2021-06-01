import styles from './recommendation.css';
import { useState, useEffect } from 'react';
import { Cascader, Table, Button } from 'antd';

export default function Recommendation() {
    // Item selecter
    // TODO: Get item id from back end
    const [itemId, setItemId] = useState('');
    const [item, setItem] = useState({}); // Item information of current selected item
    const options = [
      {
        value: '1003461',
        label: '1003461',
      }
    ];

    function itemIdOnChange(value) {
      setItemId(value[0]);
    };

    // Recommendation data from back end (table-like json)
    const [dataSource, setDataSource] = useState([]);
    const [columns, setColumns] = useState([]);
    
    // Get table-like json from back-end
    useEffect(()=>{
      if (itemId === '' || itemId === undefined) {
        setItem({});
        return;
      }

      fetch(`/api/get-item/${itemId}`).then(res => res.json()).then(data => {
        setItem(data);
      })

      fetch(`/api/nearest-items/${itemId}`).then(res => res.json()).then(data => {
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
    }, [itemId]);

    return (
        <div>
            <h1 className={styles.title}>Recommendation</h1>
            <table width='100%'>
              <tbody>
                <tr>
                  <td width='20%'>
                    <Cascader 
                      options={options}
                      onChange={itemIdOnChange}
                      placeholder="Please select the item id you want to analyze"
                    />
                  </td>

                  <td width='80%'>
                    <Table 
                      dataSource={dataSource}
                      columns={columns}
                      title={() => {
                        return (
                          <table>
                            <tbody>
                              <td>Nearest items for item_id:<Button type='primary'>{itemId}</Button></td>
                              <td>category:<Button type='dashed'>{item['category_code']}</Button></td>
                              <td>brand:<Button type='dashed'>{item['brand']}</Button></td>
                            </tbody>
                          </table>
                        )}}
                      scroll={{ y: 240 }}
                    />
                  </td>
                </tr>
              </tbody>
            </table>
        </div>
    );
}