using System;
using System.Collections.Generic;
using Xam_SmartHouse.ViewModels;
using Xam_SmartHouse.Views;
using Xamarin.Forms;

namespace Xam_SmartHouse
{
    public partial class AppShell : Xamarin.Forms.Shell
    {
        public AppShell()
        {
            InitializeComponent();
          
        
        }

        private async void OnMenuItemClicked(object sender, EventArgs e)
        {
            await Shell.Current.GoToAsync("//LoginPage");
        }
    }
}
