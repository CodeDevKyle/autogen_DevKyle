using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Hosting;

namespace Microsoft.AutoGen.Agents.Runtime;

public static class Host
{
    public static async Task<WebApplication> StartAsync(bool local = false)
    {
        var builder = WebApplication.CreateBuilder();
        if (local)
        {
            builder.AddLocalAgentService();
        }
        else
        {
            builder.AddAgentService();
        }
        builder.AddServiceDefaults();
        var app = builder.Build();
        app.MapAgentService();
        await app.StartAsync().ConfigureAwait(false);
        return app;
    }
}
