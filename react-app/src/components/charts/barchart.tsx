import React from 'react';
import ReactDOM from 'react-dom';
import { Vega } from 'react-vega';

export default function BarChart(props) {
    return (<Vega spec={props.spec}></Vega>);
}