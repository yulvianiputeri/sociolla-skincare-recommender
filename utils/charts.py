import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_rating_chart(data):
    """
    Membuat grafik rating produk
    """
    try:
        rating_counts = data['rating'].value_counts().sort_index()
        
        fig = go.Figure(data=[
            go.Bar(
                x=rating_counts.index,
                y=rating_counts.values,
                marker_color='#FF69B4',
                text=rating_counts.values,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Distribusi Rating Produk",
            xaxis_title="Rating",
            yaxis_title="Jumlah Produk",
            template="plotly_white",
            bargap=0.2
        )
        
        return fig
    except Exception as e:
        st.error(f"Error membuat grafik rating: {str(e)}")
        return None

def create_price_chart(data):
    """
    Membuat grafik distribusi harga
    """
    try:
        fig = px.box(
            data,
            x='category',
            y='price',
            color='category',
            title="Distribusi Harga per Kategori",
            labels={
                'category': 'Kategori',
                'price': 'Harga (Rp)'
            }
        )
        
        fig.update_layout(
            xaxis_title="Kategori",
            yaxis_title="Harga (Rp)",
            showlegend=False
        )
        
        return fig
    except Exception as e:
        st.error(f"Error membuat grafik harga: {str(e)}")
        return None

def create_brand_chart(data):
    """
    Membuat grafik brand terpopuler
    """
    try:
        # Hitung total review dan rating rata-rata per brand
        brand_analysis = data.groupby('brand').agg({
            'number_of_reviews': 'sum',
            'rating': 'mean',
            'product_name': 'count'
        }).round(2)
        
        brand_analysis = brand_analysis.sort_values('number_of_reviews', ascending=False).head(10)
        
        fig = go.Figure()
        
        # Tambahkan bar untuk jumlah review
        fig.add_trace(go.Bar(
            x=brand_analysis.index,
            y=brand_analysis['number_of_reviews'],
            name='Jumlah Review',
            marker_color='#FF69B4'
        ))
        
        # Tambahkan line untuk rating
        fig.add_trace(go.Scatter(
            x=brand_analysis.index,
            y=brand_analysis['rating'],
            name='Rating Rata-rata',
            yaxis='y2',
            line=dict(color='#FFD700', width=2)
        ))
        
        fig.update_layout(
            title="10 Brand Terpopuler (Review & Rating)",
            xaxis_title="Brand",
            yaxis_title="Jumlah Review",
            yaxis2=dict(
                title="Rating",
                overlaying="y",
                side="right"
            ),
            template="plotly_white",
            barmode='group'
        )
        
        return fig
    except Exception as e:
        st.error(f"Error membuat grafik brand: {str(e)}")
        return None

def create_category_rating_chart(data):
    """
    Membuat grafik rating per kategori
    """
    try:
        category_stats = data.groupby('category').agg({
            'rating': ['mean', 'count', 'std'],
            'price': 'mean'
        }).round(2)
        
        category_stats.columns = ['rating_mean', 'product_count', 'rating_std', 'price_mean']
        category_stats = category_stats.sort_values('rating_mean', ascending=False)
        
        fig = go.Figure()
        
        # Bar untuk rating rata-rata
        fig.add_trace(go.Bar(
            x=category_stats.index,
            y=category_stats['rating_mean'],
            name='Rating Rata-rata',
            marker_color='#FF69B4',
            error_y=dict(
                type='data',
                array=category_stats['rating_std'],
                visible=True
            )
        ))
        
        # Scatter untuk jumlah produk
        fig.add_trace(go.Scatter(
            x=category_stats.index,
            y=category_stats['product_count'],
            name='Jumlah Produk',
            yaxis='y2',
            mode='markers',
            marker=dict(
                size=10,
                color='#FFD700'
            )
        ))
        
        fig.update_layout(
            title="Analisis Rating per Kategori",
            xaxis_title="Kategori",
            yaxis_title="Rating Rata-rata",
            yaxis2=dict(
                title="Jumlah Produk",
                overlaying="y",
                side="right"
            ),
            template="plotly_white",
            showlegend=True
        )
        
        return fig
    except Exception as e:
        st.error(f"Error membuat grafik kategori: {str(e)}")
        return None

def create_price_range_analysis(data):
    """
    Membuat analisis berdasarkan range harga
    """
    try:
        # Buat kategori harga
        data['price_range'] = pd.qcut(data['price'], q=5, labels=[
            'Sangat Murah', 'Murah', 'Menengah', 'Mahal', 'Sangat Mahal'
        ])
        
        price_analysis = data.groupby('price_range').agg({
            'rating': 'mean',
            'number_of_reviews': 'mean',
            'price': ['min', 'max', 'mean']
        }).round(2)
        
        fig = go.Figure()
        
        # Bar untuk rating
        fig.add_trace(go.Bar(
            x=price_analysis.index,
            y=price_analysis[('rating', 'mean')],
            name='Rating Rata-rata',
            marker_color='#FF69B4'
        ))
        
        # Line untuk jumlah review
        fig.add_trace(go.Scatter(
            x=price_analysis.index,
            y=price_analysis[('number_of_reviews', 'mean')],
            name='Review Rata-rata',
            yaxis='y2',
            line=dict(color='#FFD700', width=2)
        ))
        
        fig.update_layout(
            title="Analisis Rating & Review Berdasarkan Range Harga",
            xaxis_title="Range Harga",
            yaxis_title="Rating Rata-rata",
            yaxis2=dict(
                title="Jumlah Review Rata-rata",
                overlaying="y",
                side="right"
            ),
            template="plotly_white"
        )
        
        return fig
    except Exception as e:
        st.error(f"Error membuat analisis range harga: {str(e)}")
        return None

def create_repurchase_analysis(data):
    """
    Membuat analisis tingkat pembelian ulang
    """
    try:
        if all(col in data.columns for col in ['repurchase_yes', 'repurchase_no', 'repurchase_maybe']):
            repurchase_data = data.groupby('category').agg({
                'repurchase_yes': 'sum',
                'repurchase_no': 'sum',
                'repurchase_maybe': 'sum'
            })
            
            # Hitung persentase
            repurchase_total = repurchase_data.sum(axis=1)
            repurchase_pct = repurchase_data.div(repurchase_total, axis=0) * 100
            
            fig = go.Figure()
            
            # Stacked bar untuk setiap kategori repurchase
            fig.add_trace(go.Bar(
                x=repurchase_pct.index,
                y=repurchase_pct['repurchase_yes'],
                name='Ya',
                marker_color='#32CD32'
            ))
            
            fig.add_trace(go.Bar(
                x=repurchase_pct.index,
                y=repurchase_pct['repurchase_maybe'],
                name='Mungkin',
                marker_color='#FFD700'
            ))
            
            fig.add_trace(go.Bar(
                x=repurchase_pct.index,
                y=repurchase_pct['repurchase_no'],
                name='Tidak',
                marker_color='#FF4500'
            ))
            
            fig.update_layout(
                title="Analisis Pembelian Ulang per Kategori",
                xaxis_title="Kategori",
                yaxis_title="Persentase (%)",
                barmode='stack',
                template="plotly_white"
            )
            
            return fig
    except Exception as e:
        st.error(f"Error membuat analisis pembelian ulang: {str(e)}")
        return None