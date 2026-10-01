"""Add a read-only Photos snapshot endpoint to the pinned WDA source."""
from pathlib import Path
import plistlib

source=Path('wda/WebDriverAgentLib/Commands/FBTouchActionCommands.m')
text=source.read_text()
anchor='    [[FBRoute POST:@"/wda/import-media"].withoutSession respondWithTarget:self action:@selector(handleImportMedia:)],'
assert text.count(anchor)==1
text=text.replace(anchor,anchor+'\n    [[FBRoute GET:@"/wda/phonefarm-library"].withoutSession respondWithTarget:self action:@selector(handlePhoneFarmLibrary:)],')
method='''
+ (id<FBResponsePayload>)handlePhoneFarmLibrary:(FBRouteRequest *)request
{
  // Do not prompt or return an incomplete library under limited permission.
  if ([PHPhotoLibrary authorizationStatusForAccessLevel:PHAccessLevelReadWrite] != PHAuthorizationStatusAuthorized) {
    return FBResponseWithObject(@{ @"error": @"full_photos_access_required" });
  }
  PHFetchResult<PHAssetCollection *> *collections = [PHAssetCollection fetchAssetCollectionsWithType:PHAssetCollectionTypeSmartAlbum subtype:PHAssetCollectionSubtypeSmartAlbumUserLibrary options:nil];
  PHAssetCollection *library = collections.firstObject;
  if (!library) return FBResponseWithObject(@{ @"error": @"library_unavailable" });
  PHFetchOptions *options = [PHFetchOptions new];
  options.includeHiddenAssets = NO;
  // Expose Photos' native collection order; do not invent a date sort.
  PHFetchResult<PHAsset *> *assets = [PHAsset fetchAssetsInAssetCollection:library options:options];
  NSMutableArray *items = [NSMutableArray new];
  [assets enumerateObjectsUsingBlock:^(PHAsset *asset, NSUInteger index, BOOL *stop) {
    [items addObject:@{ @"id": asset.localIdentifier, @"index": @(index), @"mediaType": @(asset.mediaType) }];
  }];
  return FBResponseWithObject(@{ @"schema": @1, @"order": @"photos_user_library_native", @"count": @(items.count), @"assets": items });
}

'''
anchor='+ (id<FBResponsePayload>)handleImportMedia:'
assert text.count(anchor)==1
text=text.replace(anchor,method+anchor)
source.write_text(text)
plist=Path('wda/WebDriverAgentRunner/Info.plist')
data=plistlib.loads(plist.read_bytes())
data['NSPhotoLibraryUsageDescription']='Read Photos asset positions for PhoneFarm media mapping.'
plist.write_bytes(plistlib.dumps(data))
