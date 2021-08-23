using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Xam_SmartHouse.Models;

namespace Xam_SmartHouse.Services
{
    public class MockDataStore : IDataStore<People>
    {
        readonly List<People> items;

        public MockDataStore()
        {
           
        }

        public async Task<bool> AddItemAsync(People item)
        {
            items.Add(item);

            return await Task.FromResult(true);
        }

        public async Task<bool> UpdateItemAsync(People item)
        {
            var oldItem = items.Where((People arg) => arg.name == item.name).FirstOrDefault();
            items.Remove(oldItem);
            items.Add(item);

            return await Task.FromResult(true);
        }

        public async Task<bool> DeleteItemAsync(string name)
        {
            var oldItem = items.Where((People arg) => arg.name == name).FirstOrDefault();
            items.Remove(oldItem);

            return await Task.FromResult(true);
        }

        public async Task<People> GetItemAsync(string name)
        {
            return await Task.FromResult(items.FirstOrDefault(s => s.name == name));
        }

        public async Task<IEnumerable<People>> GetItemsAsync(bool forceRefresh = false)
        {
            return await Task.FromResult(items);
        }
    }
}