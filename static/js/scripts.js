/*
 * ===============================================================
 * CASTAWAYS ICE CREAM SHOP - FREELANCER THEME SCRIPTS
 * ===============================================================
 * 
 * Core JavaScript functionality for the homepage theme including:
 * - Responsive navigation behavior and scrollspy
 * - Navbar shrinking on scroll
 * - Bootstrap component initialization
 * - Mobile navigation handling
 * 
 * Based on: Start Bootstrap Freelancer v7.0.7
 * Dependencies: Bootstrap 5 JavaScript bundle
 * Author: Start Bootstrap / Customized for Castaways
 * ===============================================================
 */

/*!
* Start Bootstrap - Freelancer v7.0.7 (https://startbootstrap.com/theme/freelancer)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-freelancer/blob/master/LICENSE)
*/

// ============================================================================
// MAIN THEME INITIALIZATION
// ============================================================================

window.addEventListener('DOMContentLoaded', event => {

    // ========================================
    // RESPONSIVE NAVIGATION FUNCTIONALITY  
    // ========================================
    
    // Navbar shrink function - adds styling when user scrolls
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Initialize navbar shrinking effect
    navbarShrink();

    // Apply shrinking effect when user scrolls
    document.addEventListener('scroll', navbarShrink);

    // ========================================
    // BOOTSTRAP SCROLLSPY INITIALIZATION
    // ========================================
    
    // Activate Bootstrap scrollspy on the main navigation
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // ========================================
    // MOBILE NAVIGATION HANDLING
    // ========================================
    
    // Auto-collapse navbar when navigation links are clicked on mobile
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});
