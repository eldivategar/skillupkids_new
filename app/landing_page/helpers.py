from app.models import Member, Mitra, ActivityList
from asgiref.sync import sync_to_async

async def get_achievements(request):
    try:
        # count total member
        total_member = await sync_to_async(Member.objects.count)()
        # count total mitra
        total_mitra = await sync_to_async(Mitra.objects.count)()
        # count total activity
        total_activity = await sync_to_async(ActivityList.objects.count)()
        context = {
            'total_member': total_member,
            'total_mitra': total_mitra,
            'total_activity': total_activity,
        }
        return context
    except Exception as e:
        return 'Gagal mengambil data pencapaian: ' + str(e)
