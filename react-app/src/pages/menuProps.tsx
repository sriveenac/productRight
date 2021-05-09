import React, { CSSProperties } from 'react';
import {
    HomeOutlined,
    BarChartOutlined,
    FundOutlined
} from '@ant-design/icons';

export default {
    title: 'ProductRight',
    logo: 'placeholder',

    menuItemRender: (item, dom) => (
        <i>
            <a href={item.path} style={{color: 'white'}}>
                {dom}
            </a>
        </i>
    ),

    route: {
        path: '/menu',

        routes: [
            {
                path: '/',
                name: 'Home',
                icon: <HomeOutlined />,
                component: './',
            },
            {
                path: '/analysis',
                name: 'Analysis',
                icon: <BarChartOutlined />,
                component: './analysis',
            },
            {
                path: '/recommendation',
                name: 'Recommendation',
                icon: <FundOutlined />,
                component: './recommendation',
            },
        ],
    },

    location: {
        pathname: '/',
    },
};