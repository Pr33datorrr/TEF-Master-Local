"""
TEF Master Local - Resource Library Module
Curated TEF resources with search and favorites.
"""

import streamlit as st
from database import db
from data.resources import (
    get_all_resources, get_resources_by_category, 
    search_resources, get_all_categories
)


def render_resources():
    """Main Resource Library interface."""
    st.header("📚 Ultimate Resource Library")
    st.markdown("Curated free resources for TEF preparation")
    
    # Search bar
    search_query = st.text_input("🔍 Search resources", placeholder="Try 'grammar' or 'podcast'")
    
    # Category filter
    col1, col2 = st.columns([2, 1])
    with col1:
        categories = ["All Categories"] + get_all_categories()
        selected_category = st.selectbox("Filter by category", categories)
    
    with col2:
        show_favorites_only = st.checkbox("⭐ Favorites Only")
    
    st.markdown("---")
    
    # Get resources
    if search_query:
        resources = search_resources(search_query)
    elif selected_category != "All Categories":
        resources = get_resources_by_category(selected_category)
    else:
        resources = get_all_resources()
    
    # Filter favorites
    user_favorites = db.get_favorites()
    if show_favorites_only:
        resources = [r for r in resources if r["id"] in user_favorites]
    
    # Display resources
    if not resources:
        st.info("No resources found. Try a different search or category.")
    else:
        st.markdown(f"**{len(resources)} resources found**")
        
        for resource in resources:
            render_resource_card(resource, resource["id"] in user_favorites)


def render_resource_card(resource: dict, is_favorite: bool):
    """Render a single resource card."""
    resource_id = resource["id"]
    
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"### [{resource['title']}]({resource['url']})")
            st.caption(f"**Category:** {resource['category']}")
            st.markdown(resource['description'])
        
        with col2:
            # Favorite button
            if is_favorite:
                if st.button("⭐", key=f"fav_{resource_id}"):
                    db.remove_favorite(resource_id)
                    st.rerun()
            else:
                if st.button("☆", key=f"fav_{resource_id}"):
                    db.add_favorite(resource_id)
                    st.rerun()
        
        st.markdown("---")


# ==================== EXTENSIBILITY INFO ====================
def show_add_resource_info():
    """Display information on how to add new resources."""
    st.info("""
    **Want to add your own resources?**
    
    1. Open `data/resources.py`
    2. Add a new entry to the `RESOURCES` list:
    ```python
    {
        "id": "category_xxx",
        "category": "Category Name",
        "title": "Resource Title",
        "url": "https://example.com",
        "description": "Brief description"
    }
    ```
    3. Save the file - changes appear immediately!
    
    See the file for detailed examples.
    """)
