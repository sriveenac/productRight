import React, { CSSProperties } from 'react';
import {
    HomeOutlined,
    BarChartOutlined,
    FundOutlined
} from '@ant-design/icons';
import { Link } from 'react-router-dom';

export default {
    title: 'ProductRight',
    logo: 'https://raw.githubusercontent.com/BrandNewLifeJackie26/productRight/dev/placeholder.png',

    menuItemRender: (item, dom) => (
        <i>
            <Link to={item.path} style={{color: 'white'}}>
                {dom}
            </Link>
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